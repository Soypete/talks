#!/bin/bash
# Record the side-by-side replay as a silent video. Run this from a Terminal window you have sized and
# styled for the video (big font, ~140x34). macOS asks for Screen Recording permission the first time.
#
#   ./record_video.sh                 # whole main display
#   REGION=x,y,w,h ./record_video.sh  # just a rectangle (points), e.g. the terminal window
#   DISPLAY_NUM=2 ./record_video.sh   # record that display (screencapture -D); default is the main display
#
# No audio is recorded (screencapture only captures sound with -g). Also writes a .mp4 next to the .mov.
set -euo pipefail
cd "$(dirname "$0")"
TAKE="${TAKE:-takes/take-1002.json}"
OUT="${OUT:-out/guardrails-demo.mov}"
LEAD=2; HOLD=5
DUR=$(python3 -c "import json,sys; d=json.load(open('$TAKE')); print(int(max(p['duration'] for p in d['panes'])) + $LEAD + $HOLD + 3)")
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
echo "Recording ${DUR}s to $OUT ..."
screencapture -v -V "$DUR" ${DISPLAY_NUM:+-D "$DISPLAY_NUM"} ${REGION:+-R "$REGION"} "$OUT" &
CAP=$!
sleep 1.5
python3 live_demo.py replay "$TAKE" --lead-in "$LEAD" --hold "$HOLD"
wait "$CAP" || { echo "screencapture failed (Screen Recording permission?)" >&2; exit 1; }
./convert_mp4.sh "$OUT"
