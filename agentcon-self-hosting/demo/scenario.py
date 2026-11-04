"""A Scenario is everything the engine needs to run one multi-step task."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol


class Workspace(Protocol):
    """Mutable task state. One fresh instance per run."""

    steps: list[str]
    final: str | None

    def run(self, tool: str, args: dict[str, Any]) -> tuple[str, str | None]:
        """Execute a tool. Return (output, error); exactly one is non-empty."""

    def score(self) -> float:
        """Accuracy in [0, 1], called once after the terminal tool is accepted."""


@dataclass(frozen=True)
class Scenario:
    name: str
    system_prompt: str
    task: str
    tools: list[dict[str, Any]]
    new_workspace: Callable[[], Workspace]
    required_steps: list[str]
    terminal_tool: str
    prerequisites: list[dict[str, str]] = field(default_factory=list)
    nudges: dict[str, str] = field(default_factory=dict)
