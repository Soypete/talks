"""Two-column terminal view for the side-by-side demo. Pure rendering; no I/O."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_ANSI = re.compile(r"\x1b\[[0-9;]*m")
RESET, BOLD, DIM = "\x1b[0m", "\x1b[1m", "\x1b[2m"
RED, GREEN, YELLOW, CYAN = "\x1b[31m", "\x1b[32m", "\x1b[33m", "\x1b[36m"
SEPARATOR = " │ "


@dataclass
class Pane:
    title: str
    lines: list[str] = field(default_factory=list)
    status: str = ""


def visible_len(text: str) -> int:
    return len(_ANSI.sub("", text))


def _fit(text: str, width: int) -> str:
    """Truncate by visible width (keeping color codes intact), then pad to exactly width."""
    out, seen, i = [], 0, 0
    while i < len(text) and seen < width:
        m = _ANSI.match(text, i)
        if m:
            out.append(m.group())
            i = m.end()
            continue
        out.append(text[i])
        seen += 1
        i += 1
    return "".join(out) + RESET + " " * (width - seen)


def _color(line: str) -> str:
    if line.startswith(("✓", "✗")):
        return (GREEN if line.startswith("✓") else RED) + BOLD + line + RESET
    if line.startswith("nudge"):
        return YELLOW + BOLD + "↳ " + line + RESET
    if "error" in line:
        return RED + line + RESET
    if line.startswith("rescued"):
        return CYAN + line + RESET
    if line.endswith("-> ok"):
        return line[: -len("ok")] + GREEN + "ok" + RESET
    return line


def render(panes: list[Pane], width: int, height: int) -> str:
    """height rows x width visible columns: title, status, rule, then the latest lines of each pane."""
    col = (width - len(SEPARATOR) * (len(panes) - 1)) // len(panes)
    body_rows = height - 3
    cells: list[list[str]] = []
    for p in panes:
        tail = p.lines[-body_rows:]
        cells.append(
            [BOLD + p.title + RESET, DIM + p.status + RESET, DIM + "─" * col + RESET]
            + [_color(line) for line in tail]
            + [""] * (body_rows - len(tail))
        )
    rows = []
    for r in range(height):
        parts = [_fit(c[r], col) for c in cells]
        row = (DIM + SEPARATOR + RESET).join(parts)
        rows.append(row + " " * (width - visible_len(row)))
    return "\n".join(rows)
