#!/bin/bash
cd ~/code/misc/talks/agentcon-self-hosting/demo || exit 1
export LLM_BASE_URL=http://127.0.0.1:8081/v1 LLM_MODEL=gpt-oss-20b
rm -f runs/oss2-*.jsonl runs/oss2-*.err runs/OSS2DONE
for n in 1 2 3 4; do python3 probe.py 10 --scenario "coding:$n" --no-parallel >> "runs/oss2-ladder-$n.jsonl" 2>> "runs/oss2-ladder-$n.err"; done
python3 probe.py 10 --scenario kei_provisioning --no-parallel >> runs/oss2-kei.jsonl 2>> runs/oss2-kei.err
echo done > runs/OSS2DONE
