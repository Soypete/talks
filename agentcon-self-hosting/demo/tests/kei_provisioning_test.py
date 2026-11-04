"""Kei-flavored provisioning scenario: an in-memory mock where every step needs an opaque id."""

import json
import re

import pytest

import scenarios
from scenarios.kei_provisioning import SCENARIO, make_scenario, solve_script
from workflow import Mode, run_workflow

ID = re.compile(r"\b(?:grp|pol|con)_[a-z0-9]{6}\b")


def new(seed: int = 7):
    return make_scenario(seed).new_workspace()


def ok(ws, tool, **args):
    out, err = ws.run(tool, args)
    assert err is None, err
    return out


def bad(ws, tool, **args):
    out, err = ws.run(tool, args)
    assert out == "" and err, (out, err)
    return err


def ident(text: str) -> str:
    found = ID.findall(text)
    assert len(found) == 1, text
    return found[0]


def provision(ws, actions="read", kind="http_api", cname="crm", bob=False):
    grp = ident(ok(ws, "create_group", name="data-science"))
    ok(ws, "add_member", group_id=grp, user="alice")
    if bob:
        ok(ws, "add_member", group_id=grp, user="bob")
    con = ident(ok(ws, "create_connector", name=cname, kind=kind))
    pol = ident(ok(ws, "create_policy", group_id=grp, connector_id=con, actions=actions))
    return grp, con, pol


def verify(ws, con):
    return [
        ok(ws, "authorize", user="alice", connector_id=con, action="read"),
        ok(ws, "authorize", user="alice", connector_id=con, action="write"),
        ok(ws, "authorize", user="bob", connector_id=con, action="read"),
    ]


# ---- 1. workspace level ----------------------------------------------------------------------


def test_ids_are_deterministic_per_seed_and_differ_across_seeds():
    a, b, c = new(7), new(7), new(8)
    ids = [ident(ok(w, "create_group", name="g")) for w in (a, b, c)]
    assert ids[0] == ids[1] != ids[2]
    assert ids[0].startswith("grp_")
    assert ident(ok(a, "create_connector", name="crm", kind="http_api")).startswith("con_")


def test_happy_path_state_and_score():
    ws = new()
    grp, con, pol = provision(ws)
    assert pol.startswith("pol_")
    assert verify(ws, con)[0] == "allow"
    out = ok(ws, "list_policies")
    assert pol in out and grp in out and con in out
    assert ws.steps == [
        "create_group", "add_member", "create_connector", "create_policy",
        "authorize", "authorize", "authorize", "list_policies",
    ]
    ok(ws, "done", summary="provisioned")
    assert ws.final == "provisioned"
    assert ws.steps[-1] == "done"
    assert ws.score() == 1.0


def test_authorize_outcomes_and_reasons():
    ws = new()
    _, con, _ = provision(ws)
    allow, write, bob = verify(ws, con)
    assert allow == "allow"
    assert write.startswith("deny:") and len(write) > len("deny:")
    assert bob.startswith("deny:")
    assert write != bob


def test_policy_with_write_makes_write_check_allow():
    ws = new()
    _, con, _ = provision(ws, actions="read,write")
    assert ok(ws, "authorize", user="alice", connector_id=con, action="write") == "allow"


def test_errors_are_strings_and_not_steps():
    ws = new()
    grp = ident(ok(ws, "create_group", name="data-science"))
    con = ident(ok(ws, "create_connector", name="crm", kind="http_api"))
    n = len(ws.steps)
    bad(ws, "create_group", name="data-science")
    bad(ws, "create_connector", name="crm", kind="http_api")
    bad(ws, "create_connector", name="x", kind="ftp")
    bad(ws, "add_member", group_id="grp_nope00", user="alice")
    bad(ws, "create_policy", group_id="grp_nope00", connector_id=con, actions="read")
    bad(ws, "create_policy", group_id=grp, connector_id="con_nope00", actions="read")
    bad(ws, "create_policy", group_id=grp, connector_id=con, actions="delete")
    bad(ws, "create_policy", group_id=grp, connector_id=con, actions="")
    bad(ws, "authorize", user="alice", connector_id="con_nope00", action="read")
    bad(ws, "authorize", user="alice", connector_id=con, action="admin")
    bad(ws, "no_such_tool")
    assert len(ws.steps) == n


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"actions": "read,write"}, 0.5),  # (c) fails and the write check exposes it: (d) fails
        ({"bob": True}, 0.5),  # bob in group: (a) fails and bob's read check allows -> (d) fails
        ({"kind": "github"}, 0.25),  # no crm http_api connector: only (a) holds
    ],
)
def test_partial_scores(kwargs, expected):
    ws = new()
    _, con, _ = provision(ws, **kwargs)
    verify(ws, con)
    assert ws.score() == expected


def test_wrong_connector_name_scores_partially():
    ws = new()
    _, con, _ = provision(ws, cname="other")
    verify(ws, con)
    assert ws.score() == 0.25


def test_empty_workspace_scores_zero_and_unverified_state_loses_d():
    assert new().score() == 0.0
    ws = new()
    provision(ws)
    assert ws.score() == 0.75


def test_done_requires_a_policy():
    ws = new()
    err = bad(ws, "done", summary="x")
    assert err.startswith("missing_steps:")
    assert ws.final is None


def test_done_requires_all_three_checks():
    ws = new()
    _, con, _ = provision(ws)
    assert bad(ws, "done", summary="x").startswith("unverified:")
    ok(ws, "authorize", user="alice", connector_id=con, action="read")
    ok(ws, "authorize", user="alice", connector_id=con, action="write")
    assert bad(ws, "done", summary="x").startswith("unverified:")
    ok(ws, "authorize", user="bob", connector_id=con, action="read")
    ok(ws, "done", summary="x")


def test_state_change_after_checks_invalidates_them():
    ws = new()
    grp, con, _ = provision(ws)
    verify(ws, con)
    ok(ws, "create_policy", group_id=grp, connector_id=con, actions="write")
    assert bad(ws, "done", summary="x").startswith("unverified:")
    verify(ws, con)
    ok(ws, "done", summary="x")
    assert ws.score() == 0.5  # two policies: (c) fails; alice write now allowed: (d) fails


# ---- 2. engine level -------------------------------------------------------------------------


def call(tool: str, /, **args) -> dict:
    return {"function": {"name": tool, "arguments": json.dumps(args)}}


def msg(*calls: dict, content: str = "") -> dict:
    return {"content": content, "tool_calls": list(calls)}


def scripted(*messages: dict):
    queue = list(messages)

    def chat(_messages, _tools):
        return queue.pop(0) if queue else {"content": "", "tool_calls": []}

    return chat


def script_msgs():
    return [msg(call(name, **args)) for name, args in solve_script()]


def test_solve_script_shape():
    s = solve_script()
    assert [n for n, _ in s] == [
        "create_group", "add_member", "create_connector", "create_policy",
        "authorize", "authorize", "authorize", "done",
    ]
    assert s == solve_script() != solve_script(8)


@pytest.mark.parametrize("mode", [Mode.BARE, Mode.GUARDED])
def test_perfect_run_succeeds_in_both_modes(mode):
    m = run_workflow(scripted(*script_msgs()), mode, scenario=SCENARIO)
    assert m.success, m.failure
    assert m.accuracy == 1.0
    assert m.turns == len(solve_script())
    assert m.nudges == 0


def test_bare_done_right_after_policy_fails_unverified():
    msgs = script_msgs()[:4] + [msg(call("done", summary="all set"))]
    m = run_workflow(scripted(*msgs), Mode.BARE, scenario=SCENARIO)
    assert not m.success
    assert m.failure == "unverified"


def test_guarded_policy_before_connector_is_nudged_then_recovers():
    s = solve_script()
    premature = msg(call("create_policy", group_id="grp_aaaaaa", connector_id="con_bbbbbb", actions="read"))
    msgs = [msg(call(s[0][0], **s[0][1])), msg(call(s[1][0], **s[1][1])), premature] + [msg(call(n, **a)) for n, a in s[2:]]
    m = run_workflow(scripted(*msgs), Mode.GUARDED, scenario=SCENARIO)
    assert m.nudges >= 1
    assert m.success, m.failure
    assert m.accuracy == 1.0


def test_bare_write_grant_completes_with_low_accuracy():
    s = solve_script()
    msgs = []
    for name, args in s:
        if name == "create_policy":
            args = {**args, "actions": "read,write"}
        msgs.append(msg(call(name, **args)))
    m = run_workflow(scripted(*msgs), Mode.BARE, scenario=SCENARIO)
    assert m.success, m.failure
    assert m.accuracy < 1.0


# ---- 3. well-formedness ----------------------------------------------------------------------


def test_scenario_is_well_formed_and_registered():
    names = {t["function"]["name"] for t in SCENARIO.tools}
    assert SCENARIO.terminal_tool in names
    assert set(SCENARIO.required_steps) <= names
    assert all(p["tool"] in names and p["requires"] in names for p in SCENARIO.prerequisites)
    assert {"retry", "step_blocked", "prerequisite", "fatal"} <= set(SCENARIO.nudges)
    assert scenarios.load("kei_provisioning") is SCENARIO
    assert SCENARIO.name == "kei_provisioning"
    assert "lookup" not in " ".join(names)


# ---- 4. connector name matching (found in a live run: the task says "the CRM connector") ------


@pytest.mark.parametrize("cname", ["CRM", "Crm", " crm "])
def test_connector_name_is_matched_case_insensitively(cname):
    ws = new()
    _, con, _ = provision(ws, cname=cname)
    verify(ws, con)
    ok(ws, "done", summary="granted read-only")
    assert ws.score() == 1.0


def test_done_error_names_the_missing_crm_connector_instead_of_blaming_authorize():
    ws = new()
    _, con, _ = provision(ws, cname="other")
    verify(ws, con)
    err = bad(ws, "done", summary="granted read-only")
    assert err.startswith("unverified:")
    assert "crm" in err.lower() and "http_api" in err
    assert "authorize again" not in err
