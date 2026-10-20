"""Build the talk's PNGs from the probe runs in runs/.

  python3 make_graphs.py            # writes out/*.png
Run sets are explicit so it is clear which JSONL feeds which chart.
"""

import glob
import os
import sys
from pathlib import Path

sys.path.insert(0, os.environ.get("AGENTWARE_SRC", os.path.expanduser("~/code/haikei/Agentware/python/src")))
from report import aggregate, categories, load_rows, plot_pair, plot_single
from scenarios.coding import LADDER, solve_script

HERE = Path(__file__).parent
OUT = HERE / "out"

RUNS = {
    "Qwen3.8-27B (RTX 5090)": sorted(glob.glob(str(HERE / "runs/ladder-*.jsonl"))) + [str(HERE / "runs/kei2.jsonl")],
    "gpt-oss-20B (laptop)": sorted(glob.glob(str(HERE / "runs/oss2-ladder-*.jsonl"))) + [str(HERE / "runs/oss2-kei.jsonl")],
}
FILENAMES = {"Qwen3.8-27B (RTX 5090)": "ladder-qwen3.8-27b.png", "gpt-oss-20B (laptop)": "ladder-gpt-oss-20b.png"}


def main() -> None:
    steps = {n: len(solve_script(n)) for n in LADDER}
    aggs = {name: aggregate(load_rows([Path(f) for f in files if Path(f).exists()])) for name, files in RUNS.items()}
    cats = categories({k: v for a in aggs.values() for k, v in a.items()}, steps, {"kei_provisioning": 8})
    for name, agg in aggs.items():
        plot_single(agg, cats, OUT / FILENAMES[name], f"{name}: fixing failing tests and provisioning access")
        print("wrote", OUT / FILENAMES[name])
    names = list(aggs)
    plot_pair((aggs[names[0]], names[0]), (aggs[names[1]], names[1]), cats, OUT / "ladder-both.png")
    print("wrote", OUT / "ladder-both.png")


if __name__ == "__main__":
    main()
