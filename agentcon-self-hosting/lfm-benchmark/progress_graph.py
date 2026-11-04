"""Graph matched progress-aware trials using final-state and completion metrics."""
from collections import defaultdict
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

root = Path(__file__).resolve().parent
by_mode = defaultdict(list)
for line in (root / "runs/lfm-progress-final.jsonl").read_text().splitlines():
    row = json.loads(line)
    by_mode[row["mode"]].append(row)
assert all(len(by_mode[m]) == 3 for m in ("bare", "guarded", "progress"))
labels = ["Bare", "Basic\nguardrails", "Progress-aware\nharness"]
values = [by_mode[m] for m in ("bare", "guarded", "progress")]
state = [sum(x["state_score"] for x in rows) / len(rows) * 100 for rows in values]
complete = [sum(x["success"] and x["accuracy"] == 1 for x in rows) / len(rows) * 100 for rows in values]
fig, ax = plt.subplots(figsize=(16, 9), dpi=160)
x = np.arange(3)
for offset, data, color, label in [(-.18, state, "#0f766e", "Average final-state score"), (.18, complete, "#d06b22", "Fully correct and finished")]:
    bars = ax.bar(x + offset, data, width=.32, color=color, label=label)
    for bar, value in zip(bars, data):
        ax.text(bar.get_x() + bar.get_width()/2, value + 2, f"{value:.0f}%", ha="center", va="bottom", fontsize=18, fontweight="bold")
ax.set_xticks(x, labels, fontsize=19)
ax.set_yticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"], fontsize=15)
ax.set_ylim(0, 115)
ax.grid(axis="y", alpha=.2)
ax.set_axisbelow(True)
for key in ("top", "right"):
    ax.spines[key].set_visible(False)
ax.set_title("Can a progress-aware harness help a 2B model?", loc="left", fontsize=28, pad=34, fontweight="bold")
ax.text(0, 1.015, "LFM3-Audio-2B · simulated connector task · 3 runs per mode", transform=ax.transAxes, fontsize=15, color="#555")
ax.legend(loc="upper center", bbox_to_anchor=(.5, -.15), ncol=2, frameon=False, fontsize=17)
fig.text(.5, .02, "Exploratory results: one task, three trials; model and harness evaluated together.", ha="center", fontsize=13, color="#555")
fig.tight_layout(rect=(0.03, .06, .98, .98))
fig.savefig(root / "progress-comparison.png")
