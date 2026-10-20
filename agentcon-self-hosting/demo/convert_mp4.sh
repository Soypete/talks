#!/bin/bash
# Convert a screen recording (.mov) to a 1080p H.264 .mp4 next to it, using macOS's built-in avconvert.
#   ./convert_mp4.sh out/guardrails-demo.mov   ->  out/guardrails-demo.mp4
set -euo pipefail
SRC="$1"
DST="${SRC%.*}.mp4"
rm -f "$DST"
avconvert --preset Preset1920x1080 --source "$SRC" --output "$DST" >/dev/null
ls -lh "$DST"
