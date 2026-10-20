import json
import os
import sys

SRC = os.environ.get("AGENTWARE_SRC", os.path.expanduser("~/code/haikei/Agentware/python/src"))
sys.path[:0] = [SRC, "."]

from scenarios import load
from workflow import Mode, openai_chat, run_workflow

name, mode = sys.argv[1], Mode(sys.argv[2])
log = []
inner = openai_chat("http://pedrogpt:8000/v1", "qwen3.8-27b", parallel_tool_calls=False)
def chat(messages, tools):
    msg = inner(messages, tools)
    calls = [(c["function"]["name"], c["function"]["arguments"]) for c in (msg.get("tool_calls") or [])]
    log.append({"content": (msg.get("content") or "")[:200], "calls": calls})
    return msg
m = run_workflow(chat, mode, scenario=load(name), max_turns=14)
for i, e in enumerate(log): print(i, e["calls"] or e["content"])
print(json.dumps(m.as_dict()))
