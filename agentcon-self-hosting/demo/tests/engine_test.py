"""The engine runs any Scenario; it must not know about analytics."""

import json

from scenario import Scenario
from workflow import Mode, chat_request_body, run_workflow


def call(name, **args):
    return {"function": {"name": name, "arguments": json.dumps(args)}}


def msg(*calls):
    return {"content": "", "tool_calls": list(calls)}


def scripted(*messages):
    queue = list(messages)
    return lambda _m, _t: queue.pop(0) if queue else {"content": "", "tool_calls": []}


class ToyWorkspace:
    def __init__(self):
        self.steps, self.final, self.seen = [], None, None

    def run(self, tool, args):
        if tool == "fetch":
            self.steps.append("fetch")
            return "value=42", None
        if tool == "done":
            if "fetch" not in self.steps:
                return "", "missing_steps: fetch"
            self.final = str(args.get("answer", ""))
            return "ok", None
        return "", f"unknown tool {tool!r}"

    def score(self):
        return 1.0 if self.final and "42" in self.final else 0.0


def toy_tools():
    def fn(name, **props):
        return {"type": "function", "function": {"name": name, "description": name,
                "parameters": {"type": "object", "properties": {k: {"type": "string"} for k in props}, "required": list(props)}}}
    return [fn("fetch"), fn("done", answer="")]


TOY = Scenario(
    name="toy",
    system_prompt="sys",
    task="Fetch the value then report it.",
    tools=toy_tools(),
    new_workspace=ToyWorkspace,
    required_steps=["fetch"],
    terminal_tool="done",
    prerequisites=[],
    nudges={"retry": "use a tool", "step_blocked": "fetch first"},
)


def test_engine_runs_a_custom_scenario_and_uses_its_score():
    m = run_workflow(scripted(msg(call("fetch")), msg(call("done", answer="it is 42"))), Mode.BARE, scenario=TOY)
    assert m.success and m.accuracy == 1.0 and m.turns == 2


def test_engine_passes_the_scenarios_tools_and_prompts_to_the_model():
    seen = {}

    def chat(messages, tools):
        seen["tools"] = [t["function"]["name"] for t in tools]
        seen["system"] = messages[0]["content"]
        seen["task"] = messages[1]["content"]
        return {"content": "", "tool_calls": []}

    run_workflow(chat, Mode.BARE, scenario=TOY)
    assert seen == {"tools": ["fetch", "done"], "system": "sys", "task": "Fetch the value then report it."}


def test_guarded_mode_enforces_the_scenarios_required_steps():
    m = run_workflow(
        scripted(msg(call("done", answer="guess")), msg(call("fetch")), msg(call("done", answer="42"))),
        Mode.GUARDED,
        scenario=TOY,
    )
    assert m.success and m.nudges == 1 and m.turns == 3


def test_bare_mode_reports_the_scenarios_rejection_label():
    m = run_workflow(scripted(msg(call("done", answer="guess"))), Mode.BARE, scenario=TOY)
    assert not m.success and m.failure == "missing_steps"


def test_a_wrong_answer_still_completes_but_scores_zero():
    m = run_workflow(scripted(msg(call("fetch")), msg(call("done", answer="no idea"))), Mode.BARE, scenario=TOY)
    assert m.success and m.accuracy == 0.0


def test_parallel_tool_calls_can_be_disabled_in_the_request():
    body = chat_request_body("m", [{"role": "user", "content": "x"}], [], seed=1, parallel_tool_calls=False)
    assert body["parallel_tool_calls"] is False
    assert "parallel_tool_calls" not in chat_request_body("m", [], [], seed=1)


class StateScoredWorkspace(ToyWorkspace):
    """score() reflects the work done, even if the run never signals completion."""

    def score(self):
        return 1.0 if "fetch" in self.steps else 0.0


STATE = Scenario(
    name="state",
    system_prompt="sys",
    task="t",
    tools=toy_tools(),
    new_workspace=StateScoredWorkspace,
    required_steps=["fetch"],
    terminal_tool="done",
    prerequisites=[],
    nudges={"retry": "use a tool"},
)


def test_state_score_records_correct_work_even_when_the_run_never_finishes():
    m = run_workflow(scripted(msg(call("fetch")), {"content": "All done!", "tool_calls": []}), Mode.BARE, scenario=STATE)
    assert not m.success and m.failure == "stopped_without_tool_call"
    assert m.accuracy == 0.0  # accuracy still means: finished AND correct
    assert m.state_score == 1.0  # but the work itself was right


def test_state_score_is_in_the_metrics_dict():
    m = run_workflow(scripted(msg(call("fetch")), msg(call("done", answer="42"))), Mode.BARE, scenario=STATE)
    assert m.as_dict()["state_score"] == 1.0


def test_events_show_a_short_argument_summary_for_each_tool_call():
    events = []
    run_workflow(
        scripted(msg(call("fetch")), msg(call("done", answer="the value is 42, a long answer " * 4))),
        Mode.BARE, scenario=TOY, on_event=events.append,
    )
    assert events[0] == "fetch -> ok"  # no args, no parentheses
    done = events[1]
    assert done.startswith("done(the value is 42") and done.endswith(") -> ok")
    assert len(done) < 70  # long values are truncated
