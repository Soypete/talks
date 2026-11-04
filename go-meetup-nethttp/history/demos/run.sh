#!/bin/bash
# Run real, focused examples for a live talk or recording.
set -euo pipefail
cd "$(dirname "$0")/../examples"
case "${1:-}" in
  handlers) pattern='TestPostRoute|TestMethodsAndFanout'; source=main.go; function=showPost ;;
  routing) pattern='TestMethodsAndFanout|TestDemoRouteConflict'; source=hiccups_test.go; function=TestDemoRouteConflict ;;
  channels) pattern='TestChannelHandler|TestDemoContextCancellation'; source=main.go; function=channelHandler ;;
  lifetime) pattern='TestDemoContextCancellation|TestDemoClientTimeout'; source=hiccups_test.go; function=TestDemoClientTimeout ;;
  security) pattern='TestDemoBodyLimit'; source=hiccups_test.go; function=TestDemoBodyLimit ;;
  http2) pattern='TestHTTP2'; source=main_test.go; function=TestHTTP2 ;;
  all) pattern='TestPostRoute|TestMethodsAndFanout|TestDemoRouteConflict|TestChannelHandler|TestDemoContextCancellation|TestDemoClientTimeout|TestDemoBodyLimit|TestHTTP2'; source=main.go; function=channelHandler ;;
  *) echo 'Usage: ./run.sh {handlers|routing|channels|lifetime|security|http2|all}' >&2; exit 2 ;;
esac
printf '\n--- %s: %s ---\n\n' "$source" "$function"
sed -n "/^func ${function}(/,/^}/p" "$source"
printf '\n$ go test -v -count=1 -run %q\n\n' "$pattern"
go test -v -count=1 -run "$pattern" .
