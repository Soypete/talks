#!/bin/bash
# Record Demo 2 (the benchmark against the home 5090) as a silent video. Run from a Terminal window you
# have sized and styled for the video. macOS asks for Screen Recording permission the first time.
#
#   ./record_bench.sh                 # whole main display
#   REGION=x,y,w,h ./record_bench.sh  # just a rectangle (points)
#
# The benchmark is the fixed copy in the pedro-ops worktree (TTFT counted reasoning tokens before this fix);
# set BENCH_DIR to ~/code/pedro/pedro-ops/scripts/pedrogpt/benchmark once the fix is merged.
set -euo pipefail
cd "$(dirname "$0")"
BENCH_DIR="${BENCH_DIR:-$HOME/code/pedro/pedro-ops-wt/bench-ttft/scripts/pedrogpt/benchmark}"
OUT="${OUT:-out/benchmark-demo.mov}"
CMD='go run . -url http://pedrogpt:8000/v1 -model qwen3.8-27b -n 3 -max-tokens 128'
DUR=34
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
clear
echo "Recording ${DUR}s to $OUT ..."
sleep 1
clear
screencapture -v -V "$DUR" ${DISPLAY_NUM:+-D "$DISPLAY_NUM"} ${REGION:+-R "$REGION"} "$OUT" &
CAP=$!
sleep 2
printf '$ cd pedro-ops/scripts/pedrogpt/benchmark\n$ %s\n\n' "$CMD"
(cd "$BENCH_DIR" && eval "$CMD")
sleep 5
wait "$CAP" || { echo "screencapture failed (Screen Recording permission?)" >&2; exit 1; }
./convert_mp4.sh "$OUT"
