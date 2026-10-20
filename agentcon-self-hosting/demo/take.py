"""A recorded take: each pane's timestamped events, replayable on its own clock. Pure; no I/O except save/load."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from live_view import Pane


@dataclass
class PaneTake:
    title: str
    events: list[tuple[float, str]]
    result: list[str]
    turns: int
    duration: float


@dataclass
class Take:
    panes: list[PaneTake]
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        return max(p.duration for p in self.panes)


def panes_at(take: Take, t: float) -> list[Pane]:
    """What each pane shows t seconds into the replay. Every pane runs on its own recorded clock."""
    out = []
    for p in take.panes:
        lines = [line for ts, line in p.events if ts <= t]
        finished = t >= p.duration
        if finished:
            lines = lines + p.result
            status = f"{p.turns} turns · {p.duration:.0f}s · done"
        else:
            calls = sum("->" in line for line in lines)
            status = f"{calls} tool calls · {t:.0f}s"
        out.append(Pane(p.title, lines, status))
    return out


def save_take(take: Take, path: Path) -> None:
    data = {
        "meta": take.meta,
        "panes": [
            {"title": p.title, "events": [[ts, line] for ts, line in p.events], "result": p.result,
             "turns": p.turns, "duration": p.duration}
            for p in take.panes
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False))


def load_take(path: Path) -> Take:
    data = json.loads(Path(path).read_text())
    panes = [
        PaneTake(p["title"], [(ts, line) for ts, line in p["events"]], p["result"], p["turns"], p["duration"])
        for p in data["panes"]
    ]
    return Take(panes, data["meta"])
