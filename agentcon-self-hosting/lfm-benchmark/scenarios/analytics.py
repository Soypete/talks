"""Scenario: analyze one podcast episode against the channel, from a real YouTube Studio export."""

from __future__ import annotations

import ast
import operator
from typing import Any

from analytics_data import TARGET_ID, Channel, Video, ground_truth, score_report
from scenario import Scenario

TASK = (
    "Analyze the podcast episode \"Your AI Isn't Secure (Here's How It Gets Hacked)\" "
    f"(video id {TARGET_ID}) against the rest of the channel. Report: its average view duration in "
    "minutes and as a percent of its length, its subscribers per 1,000 views, which long-form "
    "episode has the best retention (average view duration as a percent of length) and which has "
    "the most views, and one concrete recommendation. Compute numbers with the calculate tool."
)

SYSTEM_PROMPT = """You are a YouTube analytics assistant working in four phases. Use the tools, in order:
1. GATHER: call list_videos, then get_metrics for the target episode and for at least 2 other
   long-form episodes, and get_channel_baseline for channel totals.
2. ANALYZE: use calculate (at least 3 times) for every derived number. Average view duration in
   seconds = watch_hours * 3600 / views. Do not do arithmetic in your head.
3. DIAGNOSE: call save_findings with what the numbers say about the target episode.
4. REPORT: call submit_final with the finished report.
Long-form means longer than 60 seconds. Always respond with a tool call. Do not answer in plain text."""

MIN_VIDEOS = 3
MIN_CALCS = 3

REQUIRED_STEPS = ["list_videos", "get_metrics", "get_channel_baseline", "calculate", "save_findings"]
TERMINAL_TOOL = "submit_final"

NUDGES = {
    "retry": "That was not a valid tool call. Respond with exactly one tool call from the allowed tools.",
    "step_blocked": "You cannot finish yet. Complete the missing phases first, in order.",
    "prerequisite": "A phase was skipped. Order: list_videos, get_metrics, get_channel_baseline, calculate, save_findings, submit_final.",
    "fatal": "Too many invalid responses.",
}


def tool_schemas() -> list[dict[str, Any]]:
    def fn(name: str, desc: str, **props: str) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
                    "required": list(props),
                },
            },
        }

    return [
        fn("list_videos", "List videos with id, title, duration and views.", kind="long, short or all"),
        fn("get_metrics", "Views, watch hours, subscribers, impressions and CTR for one video.", video_id="video id"),
        fn("get_channel_baseline", "Channel-wide totals for the period."),
        fn("daily_views", "Daily view counts for one video, when available.", video_id="video id"),
        fn("calculate", "Evaluate an arithmetic expression (+ - * / ** and parentheses).", expression="expression"),
        fn("save_findings", "Save your diagnosis of the target episode.", findings="findings text"),
        fn("submit_final", "Submit the final report.", report="final report text"),
    ]


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _arith(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _arith(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _arith(node.left), _arith(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 8:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_arith(node.operand))
    raise ValueError("only numbers, + - * / ** and parentheses are allowed")


def _fmt(v: Video) -> str:
    return f"{v.id} | {v.title} | published {v.published} | {v.duration_s}s | {v.views} views"


class AnalyticsWorkspace:
    """Executes the tools over the channel export and tracks what has been done."""

    def __init__(self) -> None:
        self.channel = Channel.load()
        self.inspected: set[str] = set()
        self.calcs = 0
        self.steps: list[str] = []
        self.final: str | None = None

    def run(self, tool: str, args: dict[str, Any]) -> tuple[str, str | None]:
        """Return (output, error). Exactly one is non-empty."""
        handler = getattr(self, f"_tool_{tool}", None)
        if handler is None or tool not in {t["function"]["name"] for t in tool_schemas()}:
            return "", f"unknown tool {tool!r}"
        output, error = handler(args)
        if error is None:
            self.steps.append(tool)
        return output, error

    def _tool_list_videos(self, args: dict[str, Any]) -> tuple[str, str | None]:
        kind = str(args.get("kind", "all"))
        if kind not in {"long", "short", "all"}:
            return "", "kind must be long, short or all"
        vids = {"long": self.channel.long_form(), "all": self.channel.videos}.get(
            kind, [v for v in self.channel.videos if v.duration_s <= 60]
        )
        return "\n".join(_fmt(v) for v in vids), None

    def _tool_get_metrics(self, args: dict[str, Any]) -> tuple[str, str | None]:
        vid = str(args.get("video_id", ""))
        try:
            v = self.channel.video(vid)
        except KeyError:
            return "", f"unknown video_id {vid!r}; call list_videos for valid ids"
        self.inspected.add(vid)
        return (
            f"{v.title}: duration_s={v.duration_s} views={v.views} watch_hours={v.watch_hours} "
            f"subscribers={v.subs} impressions={v.impressions} ctr_percent={v.ctr}"
        ), None

    def _tool_get_channel_baseline(self, _args: dict[str, Any]) -> tuple[str, str | None]:
        b = self.channel.baseline
        return (
            f"views={int(b['views'])} watch_hours={b['watch_hours']} subscribers={int(b['subs'])} "
            f"impressions={int(b['impressions'])} ctr_percent={b['ctr']}"
        ), None

    def _tool_daily_views(self, args: dict[str, Any]) -> tuple[str, str | None]:
        vid = str(args.get("video_id", ""))
        rows = self.channel.daily(vid)
        if not rows:
            have = sorted({r["Content"] for r in self.channel.daily_rows})
            return "", f"no daily data for {vid!r}; available for: {', '.join(have)}"
        return "\n".join(f"{d}: {n}" for d, n in rows), None

    def _tool_calculate(self, args: dict[str, Any]) -> tuple[str, str | None]:
        expr = str(args.get("expression", ""))
        try:
            value = _arith(ast.parse(expr.strip(), mode="eval"))
        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as exc:
            return "", f"cannot calculate {expr!r}: {exc}"
        self.calcs += 1
        return f"{value:.4f}".rstrip("0").rstrip("."), None

    def _tool_save_findings(self, args: dict[str, Any]) -> tuple[str, str | None]:
        if not str(args.get("findings", "")).strip():
            return "", "save_findings requires a non-empty 'findings' argument"
        return "saved", None

    def score(self) -> float:
        return score_report(self.final or "", ground_truth(self.channel))

    def _tool_submit_final(self, args: dict[str, Any]) -> tuple[str, str | None]:
        missing = [s for s in REQUIRED_STEPS if s not in self.steps]
        if missing:
            return "", "missing_steps: " + ", ".join(missing)
        if len(self.inspected) < MIN_VIDEOS or self.calcs < MIN_CALCS:
            return "", (
                f"insufficient_research: inspect at least {MIN_VIDEOS} videos with get_metrics and "
                f"use calculate at least {MIN_CALCS} times"
            )
        report = str(args.get("report", ""))
        if not report.strip():
            return "", "submit_final requires a non-empty 'report' argument"
        self.final = report
        return "accepted", None


SCENARIO = Scenario(
    name="analytics",
    system_prompt=SYSTEM_PROMPT,
    task=TASK,
    tools=tool_schemas(),
    new_workspace=AnalyticsWorkspace,
    required_steps=REQUIRED_STEPS,
    terminal_tool=TERMINAL_TOOL,
    prerequisites=[
        {"tool": "get_metrics", "requires": "list_videos"},
        {"tool": "calculate", "requires": "get_metrics"},
        {"tool": "save_findings", "requires": "calculate"},
    ],
    nudges=NUDGES,
)
