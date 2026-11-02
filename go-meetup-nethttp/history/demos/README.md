# HTTP demos

These demos run real Go tests in `../examples` and print their commands and results. They need Go 1.24 or later. The HTTP/2 and timeout examples bind a temporary local loopback port; no external server is required.

```sh
cd go-meetup-nethttp/history/demos
./run.sh handlers  # Handler, ResponseWriter, Request; status and body
./run.sh routing   # ServeMux methods, paths, 405, Allow and conflicting routes
./run.sh lifetime  # Context cancellation and Client.Timeout
./run.sh security  # MaxBytesReader and 413
./run.sh http2     # httptest TLS server and negotiated HTTP/2
./run.sh all
```

For live demos, the example server is also available with `cd ../examples && go run .`; see its README for endpoints and flags.

## Record on macOS

The self-hosting talk used `screencapture` and `avconvert`. This workflow does the same for one demo at a time. Open a terminal, enlarge its font, and run:

```sh
./record.sh routing
# Optional: restrict recording to a rectangle in screen points:
REGION=x,y,width,height ./record.sh http2
```

Without `REGION`, the **entire display** is recorded. macOS may ask for Screen Recording permission. The default capture lasts 25 seconds; set `DURATION` to change it, and `DISPLAY_NUM` to select a display. Recordings are silent and written to the ignored `recordings/` directory as timestamped MOV and MP4 files. Watch each recording before using or sharing it. The scripts do not control other applications or use your existing server.
