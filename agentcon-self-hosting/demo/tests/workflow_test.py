"""Behavior of the 4-phase analytics workflow in bare and guarded modes.

The model is scripted: each test feeds a fixed sequence of assistant messages
so the only variable is whether guardrails wrap the loop.
"""

import json

import pytest

from analytics_data import TARGET_ID
from workflow import Mode, run_workflow


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


REPORT = (
    "Average view duration is 9.67 minutes, 22.4% of the episode. Subscribers per 1,000 views: "
    "34.3. Best retention: What AI Hardware Should You Buy. Most views: Stop Vibe Coding. "
    "Recommendation: tighten the first two minutes."
)

HAPPY = [
    msg(call("list_videos", kind="long")),
    msg(call("get_metrics", video_id=TARGET_ID)),
    msg(call("get_metrics", video_id="LZ0N6q6S1WY")),
    msg(call("get_metrics", video_id="-fvMPKLHgeY")),
    msg(call("get_channel_baseline")),
    msg(call("calculate", expression="103.2975 * 3600 / 641 / 60")),
    msg(call("calculate", expression="22 * 1000 / 641")),
    msg(call("calculate", expression="103.2975 * 3600 / 641 / 2590 * 100")),
    msg(call("save_findings", findings="Retention is the weak spot, CTR is fine.")),
    msg(call("submit_final", report=REPORT)),
]
N = len(HAPPY)


def test_bare_happy_path_succeeds_and_is_accurate():
    m = run_workflow(scripted(*HAPPY), Mode.BARE)
    assert m.success, m.failure
    assert m.turns == N == 10
    assert m.nudges == 0
    assert m.mode == "bare"
    assert m.accuracy == 1.0
    assert m.steps[0] == "list_videos" and m.steps[-1] == "submit_final"


def test_guarded_happy_path_matches_bare_when_model_behaves():
    m = run_workflow(scripted(*HAPPY), Mode.GUARDED)
    assert m.success, m.failure
    assert m.turns == N
    assert m.nudges == 0
    assert m.accuracy == 1.0


def test_a_complete_but_wrong_report_succeeds_with_low_accuracy():
    wrong = [*HAPPY[:-1], msg(call("submit_final", report="Average view duration is 5 minutes."))]
    m = run_workflow(scripted(*wrong), Mode.BARE)
    assert m.success
    assert m.accuracy == 0.0


def test_bare_stops_when_model_answers_in_text_instead_of_calling_a_tool():
    m = run_workflow(
        scripted(msg(call("list_videos", kind="long")), msg(content="Looks like retention is low.")),
        Mode.BARE,
    )
    assert not m.success
    assert m.failure == "stopped_without_tool_call"


def test_bare_fails_when_final_is_submitted_before_required_steps():
    m = run_workflow(scripted(msg(call("submit_final", report="Quick guess."))), Mode.BARE)
    assert not m.success
    assert m.failure == "missing_steps"


def test_guarded_blocks_premature_final_and_recovers():
    m = run_workflow(scripted(msg(call("submit_final", report="too early")), *HAPPY), Mode.GUARDED)
    assert m.success, m.failure
    assert m.nudges == 1
    assert m.turns == N + 1


def test_guarded_rescues_json_tool_call_written_as_text():
    text = '```json\n{"name": "list_videos", "arguments": {"kind": "long"}}\n```'
    m = run_workflow(scripted(msg(content=text), *HAPPY[1:]), Mode.GUARDED)
    assert m.success, m.failure
    assert m.rescued == 1


def test_bare_cannot_use_a_tool_call_written_as_text():
    text = '{"name": "list_videos", "arguments": {"kind": "long"}}'
    m = run_workflow(scripted(msg(content=text), *HAPPY[1:]), Mode.BARE)
    assert not m.success
    assert m.failure == "stopped_without_tool_call"


def test_guarded_nudges_a_text_only_reply_then_recovers():
    m = run_workflow(scripted(msg(content="Let me think about it."), *HAPPY), Mode.GUARDED)
    assert m.success, m.failure
    assert m.nudges == 1


def test_guarded_gives_up_after_the_retry_cap():
    m = run_workflow(scripted(*[msg(content="still no tool call")] * 10), Mode.GUARDED, max_retries=3)
    assert not m.success
    assert m.failure == "retry_limit"
    assert m.nudges == 3


def test_unknown_tool_is_reported_to_a_bare_model_as_an_error_and_loop_continues():
    m = run_workflow(scripted(msg(call("browse_web", url="x")), *HAPPY), Mode.BARE)
    assert m.success, m.failure
    assert m.turns == N + 1


def test_unknown_video_id_is_a_recoverable_tool_error():
    m = run_workflow(scripted(HAPPY[0], msg(call("get_metrics", video_id="nope")), *HAPPY[1:]), Mode.BARE)
    assert m.success, m.failure
    assert m.turns == N + 1


def test_daily_views_has_no_data_for_the_target_episode_but_does_for_others():
    seq = [HAPPY[0], msg(call("daily_views", video_id=TARGET_ID)), msg(call("daily_views", video_id="-fvMPKLHgeY")), *HAPPY[1:]]
    m = run_workflow(scripted(*seq), Mode.BARE)
    assert m.success, m.failure
    assert m.steps.count("daily_views") == 1  # only the one with data succeeded


def test_calculate_rejects_anything_but_arithmetic():
    evil = msg(call("calculate", expression="__import__('os').system('echo hi')"))
    m = run_workflow(scripted(HAPPY[0], evil, *HAPPY[1:]), Mode.BARE)
    assert m.success, m.failure
    assert m.steps.count("calculate") == 3  # the rejected one is not a completed step


def test_final_needs_three_videos_inspected_and_three_calculations():
    thin = [
        msg(call("list_videos", kind="long")),
        msg(call("get_metrics", video_id=TARGET_ID)),
        msg(call("get_channel_baseline")),
        msg(call("calculate", expression="1+1")),
        msg(call("save_findings", findings="f")),
        msg(call("submit_final", report=REPORT)),
    ]
    m = run_workflow(scripted(*thin), Mode.BARE)
    assert not m.success
    assert m.failure == "insufficient_research"


def test_guarded_blocks_calculating_before_metrics_are_fetched_and_recovers():
    early = msg(call("calculate", expression="1+1"))
    m = run_workflow(scripted(HAPPY[0], early, *HAPPY[1:]), Mode.GUARDED)
    assert m.success, m.failure
    assert m.nudges == 1
    assert m.turns == N + 1


def test_turn_budget_is_enforced():
    m = run_workflow(scripted(*[msg(call("list_videos", kind="all"))] * 50), Mode.BARE, max_turns=8)
    assert not m.success
    assert m.failure == "turn_limit"
    assert m.turns == 8


@pytest.mark.parametrize("mode", [Mode.BARE, Mode.GUARDED])
def test_metrics_report_elapsed_time_and_accuracy(mode):
    m = run_workflow(scripted(*HAPPY), mode)
    assert m.elapsed_s >= 0
    assert set(m.as_dict()) >= {"mode", "success", "turns", "nudges", "elapsed_s", "failure", "steps", "accuracy"}
