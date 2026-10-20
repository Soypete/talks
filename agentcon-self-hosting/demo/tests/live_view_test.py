import re

from live_view import Pane, render, visible_len

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def test_visible_len_ignores_ansi_color_codes():
    assert visible_len("\x1b[32mok\x1b[0m") == 2


def test_render_makes_every_row_the_same_visible_width_with_two_columns():
    left = Pane("NO GUARDRAILS", lines=["run_tests -> ok", "edit_file(a.py) -> ok"], status="turn 2 · 3s")
    right = Pane("WITH GUARDRAILS", lines=["run_tests -> ok"], status="turn 1 · 2s")
    rows = render([left, right], width=80, height=8).splitlines()
    assert len(rows) == 8
    assert {visible_len(r) for r in rows} == {80}
    assert "NO GUARDRAILS" in ANSI.sub("", rows[0]) and "WITH GUARDRAILS" in ANSI.sub("", rows[0])


def test_long_lines_are_truncated_not_wrapped_and_only_the_latest_lines_are_kept():
    pane = Pane("A", lines=[f"line {i} " + "x" * 200 for i in range(30)], status="s")
    other = Pane("B", lines=[], status="s")
    rows = [ANSI.sub("", r) for r in render([pane, other], width=60, height=10).splitlines()]
    assert all(visible_len(r) == 60 for r in rows)
    assert any("line 29" in r for r in rows) and not any("line 0 " in r for r in rows)


def test_nudge_lines_are_highlighted_and_results_are_colored():
    pane = Pane("A", lines=["nudge 1: respond with a tool call", "done -> ok"], status="s")
    out = render([pane, Pane("B", lines=[], status="")], width=60, height=6)
    assert "\x1b[33m" in out  # yellow for nudges
    assert "\x1b[32m" in out  # green for ok
