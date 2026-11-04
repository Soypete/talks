"""Run bare vs guarded N times against a live endpoint and print one JSON line per run.

  python3 probe.py 5 --scenario analytics|kei_provisioning|coding|coding:N --no-parallel
Env: LLM_BASE_URL (default http://pedrogpt:8000/v1), LLM_MODEL (default qwen3.8-27b).
"""
import argparse
import json
import os
import sys

if os.environ.get("AGENTWARE_SRC"):
    sys.path.insert(0, os.environ["AGENTWARE_SRC"])
from scenarios import load
from workflow import Mode, openai_chat, run_workflow

ap = argparse.ArgumentParser()
ap.add_argument("repeats", type=int, nargs="?", default=3)
ap.add_argument("--scenario", default="access_provisioning_v2")
ap.add_argument("--mode", choices=[m.value for m in Mode], action="append", help="mode(s) to run; default bare and guarded")
ap.add_argument("--no-parallel", action="store_true", help="send parallel_tool_calls=false")
ap.add_argument("--temperature", type=float, default=0.6, help="model profile default is 0.6")
ap.add_argument("--max-turns", type=int, default=30)
ap.add_argument("--trace", help="append detailed synthetic benchmark traces to this JSONL file")
args = ap.parse_args()

base = os.environ.get("LLM_BASE_URL", "http://pedrogpt:8000/v1")
model = os.environ.get("LLM_MODEL", "qwen3.8-27b")
if args.scenario.startswith("coding:"):
    from scenarios.coding import make_scenario
    scenario = make_scenario(int(args.scenario.split(":", 1)[1]))
else:
    scenario = load(args.scenario)
def write_trace(path, scenario, mode, run, event):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"scenario": scenario, "mode": mode, "seed": 1000 + run, **event}) + "\n")

for run in range(args.repeats):
    for mode in ([Mode(m) for m in args.mode] if args.mode else (Mode.BARE, Mode.GUARDED)):
        chat = openai_chat(
            base, model, temperature=args.temperature, seed=1000 + run,
            parallel_tool_calls=False if args.no_parallel else None,
        )
        m = run_workflow(
            chat, mode, scenario=scenario, max_turns=args.max_turns,
            on_event=lambda e: print("  ", e, file=sys.stderr, flush=True),
            on_trace=(lambda e: write_trace(args.trace, scenario.name, mode.value, run, e)) if args.trace else None,
        )
        print(json.dumps({"scenario": scenario.name, **m.as_dict()}), flush=True)
