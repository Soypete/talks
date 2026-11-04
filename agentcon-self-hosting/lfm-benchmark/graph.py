"""Plot the original paired runs and the new LFM runs (python graph.py)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from report import aggregate, categories, draw_bars, legend_handles, load_rows
from scenarios.coding import LADDER, solve_script

root = Path(__file__).resolve().parent
run = root / "runs"
models = [
    ("Qwen3.8-27B · RTX 5090", [*sorted(run.glob("ladder-*.jsonl")), run / "kei2.jsonl"]),
    ("GPT-OSS-20B · laptop", [*sorted(run.glob("oss2-ladder-*.jsonl")), run / "oss2-kei.jsonl"]),
    ("LFM3-Audio-2B Q4 · laptop", [*sorted(run.glob("lfm-ladder-*.jsonl")), run / "lfm-kei.jsonl"]),
]
aggs = [(name, aggregate(load_rows(paths))) for name, paths in models]
merged = {key: value for _, agg in aggs for key, value in agg.items()}
cats = categories(merged, {n: len(solve_script(n)) for n in LADDER}, {"kei_provisioning": 8})
fig, axes = plt.subplots(1, 3, figsize=(19.2, 10.8), dpi=150, sharey=True)
for ax, (name, agg) in zip(axes, aggs):
    draw_bars(ax, agg, cats, name)
    for text in ax.texts:
        if text.get_text().endswith("%"):
            text.set_fontsize(9)
    ax.tick_params(axis="x", labelsize=10)
axes[0].set_ylabel("Runs")
fig.legend(handles=legend_handles(), loc="lower center", ncol=2, fontsize=15, frameon=False)
fig.suptitle("Agent workflow reliability: three local models", fontsize=25, fontweight="bold", y=0.95)
fig.tight_layout(rect=(0, 0.15, 1, 0.91), w_pad=2.5)
fig.savefig(root / "comparison.png")
