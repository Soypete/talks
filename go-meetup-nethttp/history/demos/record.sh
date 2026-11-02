#!/bin/bash
# Run from a terminal styled for the talk. Screen capture requires macOS permission.
# REGION=x,y,w,h limits capture to a rectangle; otherwise the entire display is recorded.
set -euo pipefail
cd "$(dirname "$0")"
name="${1:-}"
case "$name" in handlers|routing|channels|lifetime|security|http2) ;; *) echo 'Usage: ./record.sh {handlers|routing|channels|lifetime|security|http2}' >&2; exit 2 ;; esac
mkdir -p recordings
stamp="$(date +%Y%m%d-%H%M%S)"
mov="recordings/${name}-${stamp}.mov"
mp4="recordings/${name}-${stamp}.mp4"
duration="${DURATION:-25}"
args=(-v -V "$duration")
if [[ -n "${REGION:-}" ]]; then args+=(-R "$REGION"); fi
if [[ -n "${DISPLAY_NUM:-}" ]]; then args+=(-D "$DISPLAY_NUM"); fi
printf 'Recording %s seconds to %s. ' "$duration" "$mov"
if [[ -z "${REGION:-}" ]]; then printf 'The entire display will be captured.\n'; else printf 'Capture region: %s\n' "$REGION"; fi
screencapture "${args[@]}" "$mov" &
capture=$!
sleep 2
./run.sh "$name"
wait "$capture"
avconvert --preset Preset1920x1080 --source "$mov" --output "$mp4"
printf 'Saved %s and %s\n' "$mov" "$mp4"
