"""Side-by-side terminal demo: bare vs. guardrails, same model, same task, same seed.

Each run is recorded ALONE at its true speed (running both at once would slow both), then the two
recorded timelines are replayed together at 1x. Nothing is sped up.

  python3 live_demo.py record --scenario coding:3 --seed 1002 --out runs/take-1002.json
  python3 live_demo.py replay runs/take-1002.json     # run this in the window you record

Env: LLM_BASE_URL (default http://127.0.0.1:8081/v1), LLM_MODEL (default gpt-oss-20b).
"""

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, os.environ.get("AGENTWARE_SRC", os.path.expanduser("~/code/haikei/Agentware/python/src")))
from live_view import DIM, RESET, render
from take import PaneTake, Take, load_take, panes_at, save_take
from workflow import Metrics, Mode, openai_chat, run_workflow

TITLES = {Mode.BARE: "NO GUARDRAILS", Mode.GUARDED: "WITH GUARDRAILS"}


def result_lines(m: Metrics) -> list[str]:
    if m.success and m.accuracy >= 1.0:
        return ["", f"✓ finished: all checks pass ({m.turns} turns, {m.nudges} nudges)"]
    if m.success:
        return ["", f"✗ finished but wrong (score {m.accuracy:.0%})"]
    lines = ["", f"✗ stopped: {m.failure} ({m.turns} turns)"]
    if m.state_score >= 1.0:
        lines.append("✗ the code is fixed, but the run never called done")
    return lines


def load_scenario(name: str):
    if name.startswith("coding:"):
        from scenarios.coding import make_scenario

        return make_scenario(int(name.split(":", 1)[1]))
    from scenarios import load

    return load(name)


def record_one(mode: Mode, args: argparse.Namespace) -> PaneTake:
    started = time.monotonic()
    events: list[tuple[float, str]] = []
    chat = openai_chat(args.base_url, args.model, temperature=args.temperature, seed=args.seed, parallel_tool_calls=False)
    m = run_workflow(
        chat, mode, scenario=load_scenario(args.scenario), max_turns=args.max_turns,
        on_event=lambda line: events.append((round(time.monotonic() - started, 2), line)),
    )
    return PaneTake(TITLES[mode], events, result_lines(m), m.turns, round(m.elapsed_s, 2))


def cmd_record(args: argparse.Namespace) -> None:
    panes = []
    for mode in (Mode.BARE, Mode.GUARDED):
        print(f"recording {TITLES[mode]} ...", flush=True)
        panes.append(record_one(mode, args))
        print(f"  {panes[-1].turns} turns, {panes[-1].duration:.0f}s: {panes[-1].result[-1]}", flush=True)
    meta = {"model": args.model, "scenario": args.scenario, "seed": args.seed, "temperature": args.temperature}
    save_take(Take(panes, meta), args.out)
    print("saved", args.out)


def footer(take: Take) -> str:
    m = take.meta
    return (f"{DIM}Two runs recorded separately on the same laptop, shown together at real speed · "
            f"{m.get('model')} · {m.get('scenario')} · seed {m.get('seed')}{RESET}")


def cmd_replay(args: argparse.Namespace) -> None:
    take = load_take(args.take)
    size = shutil.get_terminal_size((120, 32))
    tty = sys.stdout.isatty()
    height = size.lines - 3

    def frame(t: float) -> str:
        return render(panes_at(take, t), size.columns, height) + "\n" + footer(take)

    if not tty:
        print(frame(take.duration + 1))
        return
    sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[2J")
    try:
        sys.stdout.write("\x1b[H" + frame(0).replace("\n", "\x1b[K\n") + "\x1b[K")
        time.sleep(args.lead_in)
        start = time.monotonic()
        while (t := time.monotonic() - start) < take.duration:
            sys.stdout.write("\x1b[H" + frame(t).replace("\n", "\x1b[K\n") + "\x1b[K")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\x1b[H" + frame(take.duration + 1).replace("\n", "\x1b[K\n") + "\x1b[K")
        sys.stdout.flush()
        time.sleep(args.hold)
    finally:
        sys.stdout.write("\x1b[?25h\x1b[?1049l")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--scenario", default="coding:3")
    rec.add_argument("--seed", type=int, default=1002)
    rec.add_argument("--temperature", type=float, default=0.6)
    rec.add_argument("--max-turns", type=int, default=30)
    rec.add_argument("--base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8081/v1"))
    rec.add_argument("--model", default=os.environ.get("LLM_MODEL", "gpt-oss-20b"))
    rec.add_argument("--out", type=Path, required=True)
    rep = sub.add_parser("replay")
    rep.add_argument("take", type=Path)
    rep.add_argument("--lead-in", type=float, default=2.0, help="seconds to show the empty panes before starting")
    rep.add_argument("--hold", type=float, default=6.0, help="seconds to keep the final frame")
    args = ap.parse_args()
    {"record": cmd_record, "replay": cmd_replay}[args.cmd](args)


if __name__ == "__main__":
    main()
