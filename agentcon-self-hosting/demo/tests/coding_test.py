"""The coding scenario: a failing test suite whose bugs are revealed one at a time."""

import json

import pytest

import scenarios
from scenarios.coding import (
    LADDER,
    SCENARIO,
    CodingWorkspace,
    make_scenario,
    solve_script,
)
from workflow import Mode, run_workflow

LADDER_SIZES = (1, 2, 3, 4)


def call(name: str, **args) -> dict:
    return {"function": {"name": name, "arguments": json.dumps(args)}}


def msg(*calls: dict, content: str = "") -> dict:
    return {"content": content, "tool_calls": list(calls)}


def scripted(*messages: dict):
    queue = list(messages)

    def chat(_messages, _tools):
        if not queue:
            return {"content": "", "tool_calls": []}
        return queue.pop(0)

    return chat


def script_messages(n: int) -> list[dict]:
    return [msg(call(tool, **args)) for tool, args in solve_script(n)]


def play(ws: CodingWorkspace, steps: list[tuple[str, dict]]) -> list[tuple[str, str | None]]:
    return [ws.run(tool, args) for tool, args in steps]


@pytest.fixture
def make_ws():
    made: list[CodingWorkspace] = []

    def factory(n: int = 3) -> CodingWorkspace:
        ws = make_scenario(n).new_workspace()
        made.append(ws)
        return ws

    yield factory
    for ws in made:
        ws.close()


# --- registry / shape ---------------------------------------------------------------------


def test_registry_loads_coding_and_default_is_three_bugs():
    assert scenarios.load("coding") is SCENARIO
    assert SCENARIO.name == "coding"
    assert make_scenario(1).name == "coding-1"
    assert make_scenario(4).name == "coding-4"
    assert set(LADDER) == set(LADDER_SIZES)


def test_make_scenario_rejects_out_of_range():
    for bad in (0, 5, -1):
        with pytest.raises(ValueError):
            make_scenario(bad)


# --- workspace behaviour ------------------------------------------------------------------


def test_run_tests_initially_fails_with_a_visible_error(make_ws):
    ws = make_ws(1)
    out, err = ws.run("run_tests", {})
    assert err is None
    assert "failed" in out or "error" in out.lower()
    assert "Error" in out or "assert" in out
    assert len(out.splitlines()) <= 61


def test_edit_file_requires_exactly_one_match(make_ws):
    ws = make_ws(1)
    before, _ = ws.run("read_file", {"path": "invoice.py"})

    out, err = ws.run("edit_file", {"path": "invoice.py", "old": "no such text anywhere", "new": "x"})
    assert out == "" and "0" in err

    out, err = ws.run("edit_file", {"path": "invoice.py", "old": "sku", "new": "SKU"})
    assert out == "" and err and "occurs" in err
    assert before.count("sku") > 1
    assert str(before.count("sku")) in err

    after, _ = ws.run("read_file", {"path": "invoice.py"})
    assert after == before
    assert ws.steps == ["read_file", "read_file"]  # failed edits are not steps


def test_edit_file_applies_a_unique_match(make_ws):
    ws = make_ws(1)
    out, err = ws.run("edit_file", {"path": "invoice.py", "old": "TAX_PERCENT = 8", "new": "TAX_PERCENT = 9"})
    assert err is None and out
    body, _ = ws.run("read_file", {"path": "invoice.py"})
    assert "TAX_PERCENT = 9" in body
    assert ws.steps == ["edit_file", "read_file"]


@pytest.mark.parametrize("path", ["/etc/passwd", "../outside.py", "sub/../../x.py", "a/../../b"])
def test_paths_outside_the_project_are_rejected(make_ws, path):
    ws = make_ws(1)
    for tool, args in (
        ("read_file", {"path": path}),
        ("edit_file", {"path": path, "old": "a", "new": "b"}),
    ):
        out, err = ws.run(tool, args)
        assert out == "" and err
    assert ws.steps == []


def test_missing_file_and_unknown_tool_are_errors(make_ws):
    ws = make_ws(1)
    assert ws.run("read_file", {"path": "nope.py"})[1]
    assert ws.run("rm_rf", {})[1]


def test_test_file_is_read_only(make_ws):
    ws = make_ws(1)
    _, err = ws.run("edit_file", {"path": "test_invoice.py", "old": "assert", "new": "pass  #"})
    assert err and "read-only" in err


def test_grep_finds_matches_with_locations(make_ws):
    ws = make_ws(2)
    out, err = ws.run("grep", {"pattern": "BULK_MIN"})
    assert err is None
    assert "pricing.py:" in out
    out, err = ws.run("grep", {"pattern": "zzzz_not_there"})
    assert err is None and "no matches" in out
    assert ws.run("grep", {"pattern": "("})[1]


@pytest.mark.parametrize("n", LADDER_SIZES)
def test_bugs_are_dependent_each_fix_reveals_the_next(make_ws, n):
    ws = make_ws(n)
    script = solve_script(n)
    outputs = []
    for k in range(n):
        out, err = ws.run("run_tests", {})
        assert err is None
        outputs.append(out)
        play(ws, script[3 * k + 1 : 3 * k + 3])  # read_file, edit_file for bug k
        assert [t for t, _ in script[3 * k : 3 * k + 3]] == ["run_tests", "read_file", "edit_file"]
    final, _ = ws.run("run_tests", {})
    assert len(set(outputs)) == n, "each stage must show a different failure"
    assert all("failed" in o or "error" in o.lower() for o in outputs)
    assert final not in outputs
    assert "failed" not in final and "passed" in final


def test_first_failure_is_a_parse_error_that_masks_the_pricing_bug(make_ws):
    ws = make_ws(2)
    out, _ = ws.run("run_tests", {})
    assert "bad line" in out
    assert "pricing.py" not in out and "BULK_MIN" not in out


@pytest.mark.parametrize("n", LADDER_SIZES)
def test_score_is_one_only_after_full_solution(make_ws, n):
    ws = make_ws(n)
    assert ws.score() < 1.0
    script = solve_script(n)
    prefix_end = len(script) - 2  # everything before the final run_tests + done
    for step in script[:prefix_end]:
        play(ws, [step])
        assert ws.score() < 1.0 or step is script[prefix_end - 1]
    assert ws.score() == 1.0


def test_score_is_strictly_partial_when_some_bugs_remain(make_ws):
    ws = make_ws(3)
    play(ws, solve_script(3)[:3])
    assert 0.0 <= ws.score() < 1.0


def test_done_without_any_edit_is_rejected_as_no_changes(make_ws):
    ws = make_ws(1)
    ws.run("run_tests", {})
    out, err = ws.run("done", {"summary": "all good"})
    assert out == "" and err.startswith("no_changes:")
    assert ws.final is None


def test_done_after_edit_without_rerunning_tests_is_unverified(make_ws):
    ws = make_ws(1)
    script = solve_script(1)
    play(ws, script[:3])
    out, err = ws.run("done", {"summary": "fixed"})
    assert out == "" and err.startswith("unverified:")
    assert ws.final is None
    ws.run("run_tests", {})
    out, err = ws.run("done", {"summary": "fixed it"})
    assert err is None and out
    assert ws.final == "fixed it"


def test_done_requires_a_summary(make_ws):
    ws = make_ws(1)
    play(ws, solve_script(1)[:-1])
    assert ws.run("done", {"summary": "  "})[1]


def test_workspaces_are_isolated(make_ws):
    a, b = make_ws(1), make_ws(1)
    assert a.root != b.root
    play(a, solve_script(1)[:3])
    out_a, _ = a.run("run_tests", {})
    out_b, _ = b.run("run_tests", {})
    assert "passed" in out_a and "failed" not in out_a
    assert "failed" in out_b or "error" in out_b.lower()
    assert b.score() < 1.0 <= a.score()


def test_temp_dir_is_removed_on_close():
    ws = make_scenario(1).new_workspace()
    root = ws.root
    assert root.is_dir()
    ws.close()
    assert not root.exists()


# --- engine ------------------------------------------------------------------------------


@pytest.mark.parametrize("mode", [Mode.BARE, Mode.GUARDED])
@pytest.mark.parametrize("n", LADDER_SIZES)
def test_perfect_run_succeeds_in_both_modes(n, mode):
    m = run_workflow(scripted(*script_messages(n)), mode, scenario=make_scenario(n), max_turns=60)
    assert m.success, m.failure
    assert m.accuracy == 1.0
    assert m.nudges == 0
    assert m.steps == [t for t, _ in solve_script(n)]


def test_bare_done_without_rerunning_tests_fails_as_unverified():
    s = make_scenario(1)
    script = solve_script(1)
    msgs = [msg(call(t, **a)) for t, a in script[:3]] + [msg(call("done", summary="fixed"))]
    m = run_workflow(scripted(*msgs), Mode.BARE, scenario=s)
    assert not m.success
    assert m.failure == "unverified"


def test_bare_done_with_no_edits_fails_as_no_changes():
    msgs = [msg(call("run_tests")), msg(call("done", summary="nothing to do"))]
    m = run_workflow(scripted(*msgs), Mode.BARE, scenario=make_scenario(1))
    assert not m.success
    assert m.failure == "no_changes"


def test_guarded_edit_before_read_is_nudged_then_recovers():
    n = 1
    script = solve_script(n)
    tool, args = _edit_args(script)
    edit_first = msg(call(tool, **args))
    msgs = [edit_first, *script_messages(n)]
    m = run_workflow(scripted(*msgs), Mode.GUARDED, scenario=make_scenario(n), max_turns=30)
    assert m.nudges == 1
    assert m.success, m.failure
    assert m.accuracy == 1.0


def _edit_args(script: list[tuple[str, dict]]) -> tuple[str, dict]:
    tool, args = next(s for s in script if s[0] == "edit_file")
    return tool, args


def test_bare_edit_before_read_is_not_stopped():
    n = 1
    script = solve_script(n)
    tool, args = _edit_args(script)
    msgs = [msg(call(tool, **args))]
    m = run_workflow(scripted(*msgs), Mode.BARE, scenario=make_scenario(n))
    assert m.steps == ["edit_file"]  # bare executes it unchecked


# --- well-formedness ---------------------------------------------------------------------


@pytest.mark.parametrize("n", LADDER_SIZES)
def test_scenarios_are_well_formed(n):
    s = make_scenario(n)
    names = {t["function"]["name"] for t in s.tools}
    assert names == {"run_tests", "grep", "read_file", "edit_file", "done"}
    assert s.terminal_tool == "done" and s.terminal_tool in names
    assert set(s.required_steps) == {"run_tests", "read_file", "edit_file"} <= names
    assert s.prerequisites and all(p["tool"] in names and p["requires"] in names for p in s.prerequisites)
    assert {"retry", "step_blocked", "prerequisite", "fatal"} <= set(s.nudges)
    assert "one tool" in s.system_prompt and "tool calls" in s.system_prompt
    for t in s.tools:
        assert t["type"] == "function" and t["function"]["parameters"]["type"] == "object"


def test_solve_script_grows_with_n():
    lengths = [len(solve_script(n)) for n in LADDER_SIZES]
    assert lengths == sorted(set(lengths))
    for n in (1, 2, 3):
        assert len(solve_script(n + 1)) > len(solve_script(n))
    assert len(solve_script(1)) >= 4
    assert solve_script(3)[-1][0] == "done"
