import json

import pytest

from report import aggregate, load_rows, rung


def row(mode, ok, acc, turns=5, nudges=0, scenario="coding-2", elapsed=10.0, failure=None):
    return {"scenario": scenario, "mode": mode, "success": ok, "accuracy": acc, "turns": turns,
            "nudges": nudges, "elapsed_s": elapsed, "failure": failure}


def test_fully_correct_requires_completion_and_full_accuracy():
    rows = [row("bare", True, 1.0), row("bare", True, 0.5), row("bare", False, 0.0, failure="turn_limit"), row("bare", True, 1.0)]
    a = aggregate(rows)[("coding-2", "bare")]
    assert a["n"] == 4
    assert a["completed"] == pytest.approx(0.75)
    assert a["fully_correct"] == pytest.approx(0.5)
    assert a["mean_accuracy"] == pytest.approx((1 + 0.5 + 0 + 1) / 4)


def test_modes_and_scenarios_are_kept_apart_and_means_are_computed():
    rows = [
        row("bare", True, 1.0, turns=6, elapsed=10), row("bare", True, 1.0, turns=8, elapsed=20),
        row("guarded", True, 1.0, turns=7, nudges=2, elapsed=30),
        row("guarded", True, 1.0, scenario="coding-3"),
    ]
    agg = aggregate(rows)
    assert set(agg) == {("coding-2", "bare"), ("coding-2", "guarded"), ("coding-3", "guarded")}
    assert agg[("coding-2", "bare")]["mean_turns"] == 7
    assert agg[("coding-2", "bare")]["mean_elapsed_s"] == 15
    assert agg[("coding-2", "guarded")]["mean_nudges"] == 2


def test_failure_reasons_are_counted():
    rows = [row("bare", False, 0.0, failure="unverified"), row("bare", False, 0.0, failure="unverified"),
            row("bare", False, 0.0, failure="turn_limit")]
    assert aggregate(rows)[("coding-2", "bare")]["failures"] == {"unverified": 2, "turn_limit": 1}


def test_rung_reads_the_bug_count_from_the_scenario_name():
    assert rung("coding-4") == 4
    assert rung("coding") == 3
    assert rung("kei_provisioning") is None


def test_load_rows_skips_non_json_lines(tmp_path):
    f = tmp_path / "a.jsonl"
    f.write_text(json.dumps(row("bare", True, 1.0)) + "\nnot json\n\n")
    assert len(load_rows([f])) == 1


def test_scenario_name_for_a_rung_matches_how_the_ladder_names_scenarios():
    from report import scenario_name

    assert scenario_name(1) == "coding-1"
    assert scenario_name(3) == "coding"  # make_scenario(3) is the default scenario, named plain 'coding'
    assert rung(scenario_name(3)) == 3 and rung(scenario_name(4)) == 4


def test_state_correct_counts_runs_whose_final_state_was_right_even_if_unfinished():
    rows = [
        {**row("bare", False, 0.0, failure="stopped_without_tool_call"), "state_score": 1.0},
        {**row("bare", False, 0.0, failure="stopped_without_tool_call"), "state_score": 0.5},
        {**row("bare", True, 1.0), "state_score": 1.0},
        {**row("bare", True, 0.5), "state_score": 0.5},
    ]
    a = aggregate(rows)[("coding-2", "bare")]
    assert a["state_correct"] == pytest.approx(0.5)
    assert a["fully_correct"] == pytest.approx(0.25)


def test_rows_without_state_score_fall_back_to_accuracy_for_finished_runs():
    rows = [row("bare", True, 1.0), row("bare", False, 0.0, failure="turn_limit")]
    assert aggregate(rows)[("coding-2", "bare")]["state_correct"] == pytest.approx(0.5)


def test_category_labels_and_order_put_the_ladder_before_provisioning():
    from report import categories

    agg = aggregate([
        row("bare", True, 1.0, scenario="kei_provisioning"), row("bare", True, 1.0, scenario="coding-4"),
        row("bare", True, 1.0, scenario="coding"), row("bare", True, 1.0, scenario="coding-1"),
    ])
    assert [name for name, _ in categories(agg, {1: 5, 3: 11, 4: 14}, {"kei_provisioning": 8})] == [
        "coding-1", "coding", "coding-4", "kei_provisioning"]
    labels = [label for _, label in categories(agg, {1: 5, 3: 11, 4: 14}, {"kei_provisioning": 8})]
    assert labels[0] == "1 bug\n5 steps" and labels[-1] == "Access\nprovisioning\n8 steps"
