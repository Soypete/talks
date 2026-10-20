import json

from take import PaneTake, Take, load_take, panes_at, save_take

BARE = PaneTake(
    title="NO GUARDRAILS",
    events=[(0.5, "run_tests -> ok"), (2.0, "edit_file(a.py) -> ok"), (4.0, "run_tests -> ok")],
    result=["", "✗ stopped: stopped_without_tool_call (3 turns)"],
    turns=3,
    duration=5.0,
)
GUARDED = PaneTake(
    title="WITH GUARDRAILS",
    events=[(0.4, "run_tests -> ok"), (3.0, "nudge 1: respond with a tool call"), (5.5, "done(x) -> ok")],
    result=["", "✓ finished: all checks pass (4 turns, 1 nudges)"],
    turns=4,
    duration=6.0,
)
TAKE = Take(panes=[BARE, GUARDED], meta={"seed": 1002})


def test_only_events_that_have_happened_are_shown():
    bare, guarded = panes_at(TAKE, 2.5)
    assert bare.lines == ["run_tests -> ok", "edit_file(a.py) -> ok"]
    assert guarded.lines == ["run_tests -> ok"]


def test_each_pane_finishes_on_its_own_clock():
    bare, guarded = panes_at(TAKE, 5.2)  # bare finished at 5.0, guarded still running until 6.0
    assert bare.lines[-1].startswith("✗") and bare.status.endswith("done")
    assert not any(line.startswith("✓") for line in guarded.lines)
    assert "done" not in guarded.status
    _, guarded_end = None, panes_at(TAKE, 6.5)[1]
    assert guarded_end.lines[-1].startswith("✓")


def test_status_counts_tool_calls_and_elapsed_seconds_but_not_nudges():
    _, guarded = panes_at(TAKE, 3.5)
    assert guarded.status == "1 tool calls · 4s"  # the nudge at t=3.0 is not a tool call


def test_take_length_is_the_longest_pane():
    assert TAKE.duration == 6.0


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "take.json"
    save_take(TAKE, path)
    loaded = load_take(path)
    assert loaded == TAKE
    assert json.loads(path.read_text())["meta"]["seed"] == 1002
