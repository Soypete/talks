"""Run bare vs guarded N times against a live endpoint and print one JSON line per run.

  python3 probe.py 5 --scenario analytics|kei_provisioning|coding|coding:N --no-parallel
Env: LLM_BASE_URL (default http://pedrogpt:8000/v1), LLM_MODEL (default qwen3.8-27b).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.environ.get("AGENTWARE_SRC", os.path.expanduser("~/code/haikei/Agentware/python/src")))
from scenarios import load
from workflow import Mode, openai_chat, run_workflow

ap = argparse.ArgumentParser()
ap.add_argument("repeats", type=int, nargs="?", default=3)
ap.add_argument("--scenario", default="analytics")
ap.add_argument("--no-parallel", action="store_true", help="send parallel_tool_calls=false")
ap.add_argument("--temperature", type=float, default=0.6, help="model profile default is 0.6")
ap.add_argument("--max-turns", type=int, default=30)
args = ap.parse_args()

base = os.environ.get("LLM_BASE_URL", "http://pedrogpt:8000/v1")
model = os.environ.get("LLM_MODEL", "qwen3.8-27b")
if args.scenario.startswith("coding:"):
    from scenarios.coding import make_scenario
    scenario = make_scenario(int(args.scenario.split(":", 1)[1]))
else:
    scenario = load(args.scenario)
for run in range(args.repeats):
    for mode in (Mode.BARE, Mode.GUARDED):
        chat = openai_chat(
            base, model, temperature=args.temperature, seed=1000 + run,
            parallel_tool_calls=False if args.no_parallel else None,
        )
        m = run_workflow(
            chat, mode, scenario=scenario, max_turns=args.max_turns,
            on_event=lambda e: print("  ", e, file=sys.stderr, flush=True),
        )
        print(json.dumps({"scenario": scenario.name, **m.as_dict()}), flush=True)
