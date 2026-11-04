import json

from enhanced import ProgressTracker, compact_history, rescue_python_call, validate_calls
from scenario import Scenario
from workflow import Mode, run_workflow

TOOLS = [
    {"type": "function", "function": {"name": "read", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "done", "parameters": {"type": "object", "properties": {}, "required": []}}},
]


def test_rescue_is_literal_only_and_checks_schema():
    good = rescue_python_call('<|tool_call_start|>[read(path="a.py")]<|tool_call_end|>', {"read"})
    assert good == [{"tool": "read", "args": {"path": "a.py"}}]
    assert validate_calls(good, TOOLS) is None
    assert rescue_python_call('read(path=__import__("os").getcwd())', {"read"}) == []
    assert rescue_python_call('delete(path="a")', {"read"}) == []
    assert validate_calls([{"tool": "read", "args": {"path": 3}}], TOOLS)
    assert validate_calls([{"tool": "read", "args": {}}], TOOLS)


def test_repeated_test_results_trigger_nudge_but_changed_results_do_not():
    tracker = ProgressTracker()
    assert tracker.observe("run_tests", {}, "1 failed", None) is None
    assert tracker.observe("run_tests", {}, "1 failed", None) is None
    assert "unchanged" in tracker.observe("run_tests", {}, "1 failed", None)
    assert tracker.observe("run_tests", {}, "2 passed", None) is None


def test_compaction_keeps_task_call_ids_and_recent_diagnostics():
    messages = [{"role": "system", "content": "system"}, {"role": "user", "content": "task"}]
    for n in range(6):
        messages += [{"role": "assistant", "content": "", "tool_calls": [{"id": str(n)}]},
                     {"role": "tool", "tool_call_id": str(n), "content": "head" + "x" * 400 + "tail"}]
    result, changed = compact_history(messages, threshold_chars=100, keep_recent=4, max_old_result_chars=80)
    assert changed and result[:2] == messages[:2]
    assert [m.get("tool_call_id") for m in result if m["role"] == "tool"] == [str(i) for i in range(6)]
    assert result[-1] == messages[-1]
    assert "head" in result[3]["content"] and "tail" in result[3]["content"]
    assert messages[3]["content"] != result[3]["content"]
    again, changed_again = compact_history(result, threshold_chars=100, keep_recent=4, max_old_result_chars=80)
    assert not changed_again and again == result


def test_enhanced_sends_error_recovery_and_can_finish():
    class Workspace:
        steps = []
        final = None
        def run(self, name, args):
            self.steps.append(name)
            if name == "read":
                return "", "file missing: choose an existing path"
            self.final = "done"
            return "done", None
        def score(self):
            return 1.0
    seen = []
    def chat(messages, tools):
        seen.append(list(messages))
        name, args = ("read", {"path": "missing"}) if len(seen) == 1 else ("done", {})
        return {"content": "", "tool_calls": [{"id": str(len(seen)), "function": {"name": name, "arguments": json.dumps(args)}}]}
    scenario = Scenario("test", "system", "task", TOOLS, Workspace, [], "done")
    result = run_workflow(chat, Mode.ENHANCED, scenario=scenario)
    assert result.success and result.nudges == 1
    assert any("file missing" in m.get("content", "") and m["role"] == "user" for m in seen[1])
    assert any(m.get("role") == "tool" and m.get("tool_call_id") == "1" for m in seen[1])


def test_checklist_uses_tool_results_and_invalidates_checks_after_changes():
    from enhanced import AccessChecklist
    c = AccessChecklist()
    c.record("create_group", {"name": "data-science"}, "created group with id grp_123abc", None)
    c.record("create_connector", {"name": "crm", "kind": "http_api"}, "created connector id con_123abc", None)
    c.record("create_policy", {"group_id": "grp_123abc", "connector_id": "con_123abc", "actions": "read"}, "ok", None)
    c.record("add_member", {"group_id": "grp_123abc", "user": "alice"}, "ok", None)
    for user, action, out in [("alice", "read", "allow"), ("alice", "write", "deny: not granted"), ("bob", "read", "deny: not a member")]:
        c.record("authorize", {"user": user, "action": action, "connector_id": "con_123abc"}, out, None)
    assert c.ready()
    c.record("add_member", {"group_id": "grp_123abc", "user": "bob"}, "ok", None)
    assert not c.ready() and "checks" in c.summary().lower()


def test_progress_mode_allows_policy_before_membership_and_nudges_finish():
    from scenarios.access_provisioning_v2 import make_scenario
    from scenarios.access_provisioning_base import solve_script
    script = solve_script()
    script = [script[0], script[2], script[3], script[1], *script[4:7]]
    seen, traces = [], []
    def chat(messages, tools):
        seen.append(list(messages))
        index = len(seen) - 1
        if index == len(script):
            return {"content": "Finished", "tool_calls": []}
        name, args = script[index] if index < len(script) else ("done", {"summary": "verified"})
        return {"content": "", "tool_calls": [{"id": str(index), "function": {"name": name, "arguments": json.dumps(args)}}]}
    result = run_workflow(chat, Mode.PROGRESS, scenario=make_scenario(), on_trace=traces.append)
    assert result.success and result.accuracy == 1.0
    assert any("call done now" in m.get("content", "") for m in seen[-1] if m["role"] == "user")
    assert any(e["event"] == "tool_result" and e["tool"] == "authorize" for e in traces)
