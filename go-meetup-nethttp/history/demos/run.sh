#!/bin/bash
# Run real, focused examples for a live talk or recording.
set -euo pipefail
cd "$(dirname "$0")/../examples"
case "${1:-}" in
  handlers) pattern='TestPostRoute|TestMethodsAndFanout' ;;
  routing) pattern='TestMethodsAndFanout|TestDemoRouteConflict' ;;
  lifetime) pattern='TestDemoContextCancellation|TestDemoClientTimeout' ;;
  security) pattern='TestDemoBodyLimit' ;;
  http2) pattern='TestHTTP2' ;;
  all) pattern='TestPostRoute|TestMethodsAndFanout|TestDemoRouteConflict|TestDemoContextCancellation|TestDemoClientTimeout|TestDemoBodyLimit|TestHTTP2' ;;
  *) echo 'Usage: ./run.sh {handlers|routing|lifetime|security|http2|all}' >&2; exit 2 ;;
esac
printf '\n$ go test -v -count=1 -run %q\n\n' "$pattern"
go test -v -count=1 -run "$pattern" .
