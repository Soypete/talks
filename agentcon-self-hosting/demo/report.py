"""Aggregate probe runs; chart helpers used by make_graphs.py.

  python3 report.py runs/ladder-*.jsonl runs/kei2.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BARE_COLOR = "#c2410c"
GUARDED_COLOR = "#0f766e"


def load_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        for line in Path(path).read_text().splitlines():
            if not line.startswith("{"):
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def rung(scenario: str) -> int | None:
    """Bug count for coding scenarios ('coding' alone is the 3-bug default)."""
    if scenario == "coding":
        return 3
    m = re.fullmatch(r"coding-(\d+)", scenario)
    return int(m.group(1)) if m else None


def _state(r: dict[str, Any]) -> float:
    """Final-state score; older rows lack it, so finished runs fall back to their accuracy."""
    if "state_score" in r:
        return r["state_score"]
    return r["accuracy"] if r["success"] else 0.0


def scenario_name(r: int) -> str:
    return "coding" if r == 3 else f"coding-{r}"


def aggregate(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[(r["scenario"], r["mode"])].append(r)
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for key, rs in groups.items():
        n = len(rs)
        out[key] = {
            "n": n,
            "completed": sum(r["success"] for r in rs) / n,
            "fully_correct": sum(r["success"] and r["accuracy"] >= 1.0 for r in rs) / n,
            "state_correct": sum(_state(r) >= 1.0 for r in rs) / n,
            "mean_accuracy": sum(r["accuracy"] for r in rs) / n,
            "mean_turns": sum(r["turns"] for r in rs) / n,
            "mean_nudges": sum(r["nudges"] for r in rs) / n,
            "mean_elapsed_s": sum(r["elapsed_s"] for r in rs) / n,
            "failures": dict(Counter(r["failure"] for r in rs if r.get("failure"))),
        }
    return out


def table(agg: dict[tuple[str, str], dict[str, Any]]) -> str:
    head = f"{'scenario':<18}{'mode':<9}{'n':>3} {'correct':>8} {'done':>6} {'turns':>6} {'nudges':>7} {'sec':>6}  failures"
    lines = [head]
    for (scenario, mode), a in sorted(agg.items(), key=lambda kv: (rung(kv[0][0]) or 99, kv[0])):
        lines.append(
            f"{scenario:<18}{mode:<9}{a['n']:>3} {a['fully_correct']:>7.0%} {a['completed']:>6.0%} "
            f"{a['mean_turns']:>6.1f} {a['mean_nudges']:>7.1f} {a['mean_elapsed_s']:>6.0f}  {a['failures'] or ''}"
        )
    return "\n".join(lines)


def categories(
    agg: dict[tuple[str, str], dict[str, Any]], steps_by_rung: dict[int, int], steps_other: dict[str, int]
) -> list[tuple[str, str]]:
    """(scenario name, tick label) in display order: coding ladder rungs, then other scenarios."""
    out: list[tuple[str, str]] = []
    rungs = sorted({rung(sc) for sc, _ in agg if rung(sc)})
    for r in rungs:
        out.append((scenario_name(r), f"{r} bug{'s' if r > 1 else ''}\n{steps_by_rung.get(r, '?')} steps"))
    for name, steps in steps_other.items():
        if any(sc == name for sc, _ in agg):
            out.append((name, f"{'Access' if name == 'kei_provisioning' else name}\n{'provisioning' if name == 'kei_provisioning' else ''}\n{steps} steps"))
    return out


def draw_bars(ax: Any, agg: dict[tuple[str, str], dict[str, Any]], cats: list[tuple[str, str]], title: str) -> None:
    width = 0.36
    for i, (name, _) in enumerate(cats):
        for j, (mode, color) in enumerate((("bare", BARE_COLOR), ("guarded", GUARDED_COLOR))):
            a = agg.get((name, mode))
            if not a:
                continue
            x = i + (j - 0.5) * (width + 0.04)
            ax.bar(x, a["state_correct"] * 100, width, color=color, alpha=0.28, linewidth=0)
            ax.bar(x, a["fully_correct"] * 100, width, color=color)
            top = max(a["state_correct"], a["fully_correct"]) * 100
            ax.text(x, top + 2, f"{a['fully_correct'] * 100:.0f}%", ha="center", va="bottom", fontsize=13,
                    color=color, fontweight="bold")
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([label for _, label in cats], fontsize=13)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels([f"{v}%" for v in (0, 25, 50, 75, 100)], fontsize=13)
    ns = sorted({a["n"] for (sc, _), a in agg.items() if sc in {c for c, _ in cats}})
    sample = f"{ns[0]} runs per bar" if len(ns) == 1 else f"{ns[0]} to {ns[-1]} runs per bar"
    ax.set_title(title, fontsize=17, loc="left", pad=26)
    ax.text(0, 1.015, sample, transform=ax.transAxes, fontsize=12, color="#555", va="bottom")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def legend_handles() -> list[Any]:
    from matplotlib.patches import Patch

    return [
        Patch(color=BARE_COLOR, label="No guardrails"),
        Patch(color=GUARDED_COLOR, label="With guardrails"),
        Patch(facecolor="#777", alpha=0.28, label="Lighter: code correct at the end, but never called done"),
        Patch(facecolor="#777", label="Solid: finished and fully correct"),
    ]


def plot_single(agg: dict[tuple[str, str], dict[str, Any]], cats: list[tuple[str, str]], out: Path, title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=200)
    draw_bars(ax, agg, cats, title)
    ax.set_ylabel("Runs", fontsize=14)
    fig.legend(handles=legend_handles(), loc="lower center", ncol=2, fontsize=11, frameon=False)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)


def plot_pair(
    left: tuple[dict[tuple[str, str], dict[str, Any]], str],
    right: tuple[dict[tuple[str, str], dict[str, Any]], str],
    cats: list[tuple[str, str]],
    out: Path,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(9.6 * 2, 5.4 * 1.15), dpi=150, sharey=True)
    for ax, (agg, title) in zip(axes, (left, right)):
        draw_bars(ax, agg, cats, title)
    axes[0].set_ylabel("Runs", fontsize=14)
    fig.legend(handles=legend_handles(), loc="lower center", ncol=4, fontsize=12, frameon=False)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Print the aggregate table for probe runs.")
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args()
    print(table(aggregate(load_rows(args.files))))


if __name__ == "__main__":
    main()
