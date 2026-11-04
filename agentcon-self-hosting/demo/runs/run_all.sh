#!/bin/bash
cd ~/code/misc/talks/agentcon-self-hosting/demo || exit 1
run() { python3 probe.py "$1" --scenario "$2" --no-parallel >> "runs/$3.jsonl" 2>> "runs/$3.err"; }
rm -f runs/ladder-*.jsonl runs/ladder-*.err runs/kei2.jsonl runs/kei2.err
run 5 kei_provisioning kei2
for n in 1 2 3 4; do run 4 "coding:$n" "ladder-$n"; done
echo ALLDONE > runs/ALLDONE
