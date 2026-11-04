import re

import pytest
from scenarios import load
from scenarios.kei_provisioning import make_scenario as original
from scenarios.access_provisioning_v2 import make_scenario


def run(ws, tool, **args):
    output, error = ws.run(tool, args)
    assert not error, error
    return output


def ident(text, prefix):
    match = re.search(rf"\b{prefix}_[a-z0-9]{{6}}\b", text)
    assert match
    return match.group()


def verify(ws, cid):
    return [run(ws, "authorize", user=u, connector_id=cid, action=a) for u, a in
            (("alice", "read"), ("alice", "write"), ("bob", "read"))]


def test_corrected_scenario_is_distinct_and_requirements_explicit():
    s = load("access_provisioning_v2")
    assert s.name == "access_provisioning_v2" and "http_api" in s.task
    assert "http_api" not in original().task
    assert {"list_connectors", "update_connector"} <= {x["function"]["name"] for x in s.tools}


@pytest.mark.parametrize("wrong_kind", ["github", "google_drive"])
def test_repair_connector_then_reverify_and_finish(wrong_kind):
    ws = make_scenario().new_workspace()
    gid = ident(run(ws, "create_group", name="data-science"), "grp")
    run(ws, "add_member", group_id=gid, user="alice")
    cid = ident(run(ws, "create_connector", name="CRM", kind=wrong_kind), "con")
    run(ws, "create_policy", group_id=gid, connector_id=cid, actions="read")
    assert verify(ws, cid)[0] == "allow"
    assert ws.run("done", {"summary": "ready"})[1].startswith("unverified:")
    assert cid in run(ws, "list_connectors") and wrong_kind in run(ws, "list_connectors")
    assert ws.run("update_connector", {"connector_id": cid, "kind": "nope"})[1]
    assert ws.run("update_connector", {"connector_id": "con_bad", "kind": "http_api"})[1]
    run(ws, "update_connector", connector_id=cid, kind="http_api")
    assert "authorize again" in ws.run("done", {"summary": "ready"})[1]
    outcomes = verify(ws, cid)
    assert outcomes[0] == "allow" and outcomes[1].startswith("deny") and outcomes[2].startswith("deny")
    run(ws, "done", summary="verified")
    assert ws.score() == 1.0 and ws.final == "verified"
