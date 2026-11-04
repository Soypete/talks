"""Multi-step tool-calling engine with optional guardrails.

Phase structure ported from PedroCLI's phased agents. The same loop runs in two modes: BARE
executes whatever the model emits; GUARDED wraps every turn in agentware's
Guardrails (tool-call rescue, step enforcement, corrective nudges).
Guardrails are response quality only; they do not authorize anything.
"""

from __future__ import annotations

import json
import time
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from haikeilabs.agentware.middleware.guardrails import Guardrails, ResponseValidator

from scenario import Scenario

ChatFn = Callable[[list[dict[str, Any]], list[dict[str, Any]]], dict[str, Any]]

DEFAULT_RETRY_NUDGE = "That was not a valid tool call. Respond with exactly one tool call from the allowed tools."

class Mode(Enum):
    BARE = "bare"
    GUARDED = "guarded"


@dataclass
class Metrics:
    mode: str
    success: bool = False
    failure: str | None = None
    turns: int = 0
    nudges: int = 0
    rescued: int = 0
    elapsed_s: float = 0.0
    steps: list[str] = field(default_factory=list)
    accuracy: float = 0.0
    state_score: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "success": self.success,
            "failure": self.failure,
            "turns": self.turns,
            "nudges": self.nudges,
            "rescued": self.rescued,
            "elapsed_s": round(self.elapsed_s, 2),
            "steps": list(self.steps),
            "accuracy": round(self.accuracy, 2),
            "state_score": round(self.state_score, 2),
        }


def _parse_native(message: dict[str, Any]) -> list[dict[str, Any]]:
    calls = []
    for item in message.get("tool_calls") or []:
        fn = item.get("function", {})
        raw = fn.get("arguments", {})
        args: Any = raw
        if isinstance(raw, str):
            try:
                args = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                args = {"_invalid": raw}
        calls.append({"tool": fn.get("name", ""), "args": args if isinstance(args, dict) else {}})
    return calls


def _brief(args: dict[str, Any], limit: int = 28) -> str:
    """'(first argument value)', truncated, for one-line event logs; empty when there are no args."""
    if not args:
        return ""
    value = " ".join(str(next(iter(args.values()))).split())
    return f"({value[:limit] + '…' if len(value) > limit else value})"


def run_workflow(
    chat: ChatFn,
    mode: Mode,
    *,
    scenario: Scenario | None = None,
    max_turns: int = 20,
    max_retries: int = 3,
    on_event: Callable[[str], None] | None = None,
) -> Metrics:
    started = time.monotonic()
    metrics = Metrics(mode=mode.value)
    emit = on_event or (lambda _line: None)
    if scenario is None:
        from scenarios.analytics import SCENARIO as scenario

    ws = scenario.new_workspace()
    tools = scenario.tools
    terminal = scenario.terminal_tool
    retry_text = scenario.nudges.get("retry", DEFAULT_RETRY_NUDGE)
    guarded = mode is Mode.GUARDED
    guardrails = (
        Guardrails.from_config(
            {
                "version": 1,
                "tool_names": [t["function"]["name"] for t in tools],
                "required_steps": scenario.required_steps,
                "terminal_tool": terminal,
                "prerequisites": scenario.prerequisites,
                "nudges": scenario.nudges,
            }
        )
        if guarded
        else None
    )
    validator = ResponseValidator([t["function"]["name"] for t in tools]) if guarded else None

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": scenario.system_prompt},
        {"role": "user", "content": scenario.task},
    ]
    last_reject: str | None = None
    retries = 0
    stop_reason = "turn_limit"

    def nudge(text: str) -> bool:
        """Append a corrective user message; False when the retry cap is hit."""
        nonlocal retries
        retries += 1
        if retries > max_retries:
            return False
        metrics.nudges += 1
        emit(f"nudge {metrics.nudges}: {text}")
        messages.append({"role": "user", "content": text})
        return True

    while metrics.turns < max_turns:
        message = chat(messages, tools)
        metrics.turns += 1
        calls = _parse_native(message)
        content = message.get("content") or ""
        rescued = False

        if guarded and not calls:
            result = validator.validate_text_response(content)  # type: ignore[union-attr]
            if result.tool_calls:
                calls = [{"tool": c.tool, "args": c.args} for c in result.tool_calls]
                metrics.rescued += 1
                rescued = True
                emit("rescued tool call from text")

        if not calls:
            if not guarded:
                stop_reason = "stopped_without_tool_call"
                break
            messages.append({"role": "assistant", "content": content})
            if not nudge(retry_text):
                stop_reason = "retry_limit"
                break
            continue

        if guardrails is not None:
            verdict = guardrails.check({"tool_calls": calls})
            if verdict["outcome"] in {"retry", "step_blocked"}:
                messages.append({"role": "assistant", "content": content or json.dumps(calls)})
                text = verdict.get("nudge_text", retry_text)
                if verdict.get("missing_steps"):
                    text += " Missing: " + ", ".join(verdict["missing_steps"])
                if not nudge(text):
                    stop_reason = "retry_limit"
                    break
                continue
            if verdict["outcome"] == "fatal":
                stop_reason = "retry_limit"
                break

        retries = 0
        messages.append(
            {"role": "assistant", "content": content}
            if rescued
            else {
                "role": "assistant",
                "content": content,
                "tool_calls": message.get("tool_calls") or [],
            }
        )
        finished = False
        for index, call in enumerate(calls):
            output, error = ws.run(call["tool"], call["args"])
            emit(f"{call['tool']}{_brief(call['args'])} -> {'error: ' + error if error else 'ok'}")
            if error:
                if call["tool"] == terminal:
                    last_reject = error.split(":", 1)[0]
                if guardrails is not None:
                    recorded = guardrails.record({"tool": call["tool"], "category": "tool_error"})
                    if "nudge_text" in recorded:
                        metrics.nudges += 1
            elif guardrails is not None:
                guardrails.record({"tool": call["tool"], "args": call["args"]})
            body = f"error: {error}" if error else output
            if rescued or not message.get("tool_calls"):
                messages.append({"role": "user", "content": f"Tool result for {call['tool']}: {body}"})
            else:
                call_id = message["tool_calls"][index].get("id", f"call_{metrics.turns}_{index}")
                messages.append({"role": "tool", "tool_call_id": call_id, "content": body})
            if call["tool"] == terminal and not error:
                finished = True
        if finished:
            break

    metrics.steps = list(ws.steps)
    metrics.state_score = ws.score()
    metrics.elapsed_s = time.monotonic() - started
    if ws.final is not None:
        metrics.success = True
        metrics.accuracy = metrics.state_score
    else:
        metrics.failure = last_reject or stop_reason
    return metrics


def chat_request_body(
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    *,
    seed: int,
    temperature: float = 0.0,
    parallel_tool_calls: bool | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "temperature": temperature,
        "seed": seed,
    }
    if parallel_tool_calls is not None:
        body["parallel_tool_calls"] = parallel_tool_calls
    return body


def openai_chat(
    base_url: str,
    model: str,
    *,
    timeout: float = 300.0,
    seed: int = 42,
    temperature: float = 0.0,
    parallel_tool_calls: bool | None = None,
) -> ChatFn:
    """Chat against an OpenAI-compatible server (llama.cpp, vLLM)."""

    def chat(messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        body = json.dumps(
            chat_request_body(
                model, messages, tools, seed=seed, temperature=temperature, parallel_tool_calls=parallel_tool_calls
            )
        ).encode()
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)["choices"][0]["message"]

    return chat
