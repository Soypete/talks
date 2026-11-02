---
marp: true
theme: default
size: 16:9
paginate: true
style: |
  section { background:#0C1723; color:#F5FAFC; font-family:Arial, sans-serif; padding:54px 70px; font-size:28px; }
  section h1 { color:#F5FAFC; font-size:47px; line-height:1.09; margin:0.19em 0 0.42em; }
  section h2 { color:#D3EAF2; font-size:34px; line-height:1.3; }
  section.lead h1 {font-size:72px;margin-top:45px;color:#F5FAFC;}
  section.lead h2 {font-size:35px;line-height:1.3;color:#D3EAF2;}
  section strong { color:#58D3BC; }
  section code { color:#84DDF2; background:#172635; }
  section pre { background:#111E2C; border:1px solid #33505F; border-radius:9px; padding:17px; font-size:20px; line-height:1.23; }
  section pre code {color:#F5FAFC;background:transparent;}
  section pre code span {color:#F5FAFC;}
  section pre code .hljs-keyword, section pre code .hljs-literal {color:#FFB5E8;}
  section pre code .hljs-string {color:#A9F1BD;}
  section pre code .hljs-comment {color:#B7D3E0; font-style:italic;}
  section pre code .hljs-number, section pre code .hljs-built_in, section pre code .hljs-type {color:#FFD58A;}
  section pre code .hljs-title, section pre code .hljs-function {color:#9EE5FF;}
  section p, section li {line-height:1.24;}
  section ul {list-style-type:square;}
  section ul li {margin:0.28em 0;}
  section table {font-size:20px;width:100%;} section table th {background:#15506A;color:#F5FAFC;} section table td {background:#172635;color:#E7F5FA;}
  section blockquote {background:#112C39;color:#58D3BC;border-left:5px solid #00ADD8;padding:10px 17px;margin:16px 0;}
  section > p:first-of-type {font-size:16px;font-weight:bold;letter-spacing:1.5px;color:#00ADD8;text-transform:uppercase;}
  section > p:last-of-type {font-size:12px;color:#9BB7C6;}
  section::after {color:#7896A8;font-size:14px;}
  section.demo pre { font-size:32px; padding:24px; }
  section.demo li { font-size:32px; margin:0.5em 0; }
  section.video { padding:32px 70px; }
  section.video h1 { font-size:38px; margin:0 0 12px; }
  section.video video { display:block; width:auto; height:490px; max-width:100%; margin:auto; background:#000; }
---
<!-- _class: lead -->

**GO MEETUP | 2009–2026**

# net/http: the timeline

## Know your HTTP stack before an AI agent gaslights you

From handlers and HTTP/2 to routing, security, and testing.

<!-- SPEAKER NOTES
We will follow the package chronologically, returning to the timeline as Go adds features and then using demos to see how they work.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-0.png)

<!-- SPEAKER NOTES
Follow each release milestone, then explain the APIs and run the matching examples. The image shows every year; subsequent timeline slides progressively reveal the changes.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-1.png)

<!-- SPEAKER NOTES
Timeline stop 1: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**2012 | GO 1.0**

# http becomes net/http

**THE COMPATIBILITY PROMISE**

- March 28, 2012: Go 1 establishes a stable language and standard-library base.
- The pre-Go-1 http package moves to net/http.
- Specialized client utilities move to net/http/httputil.
- Compatibility becomes a major design constraint for future HTTP changes.

> Modern net/http is the descendant of the original Go 1 API.

*Sources: [Go 1 announcement, 28 Mar 2012](https://go.dev/blog/go1) | [Go 1 release notes](https://go.dev/doc/go1) (additional references in speaker notes)*

<!--
SPEAKER NOTES
Modern net/http is the descendant of the original Go 1 API.
SOURCE LINKS
Go 1 announcement, 28 Mar 2012 - https://go.dev/blog/go1
Go 1 release notes - https://go.dev/doc/go1
Go release history - https://go.dev/doc/devel/release
-->

---

**ANATOMY | TODAY**

# How a request gets handled

1. **Client:** `http.Client` sends a request using a `Transport`.
2. **Connection:** the transport uses HTTP/1.1 or HTTP/2.
3. **Server:** `http.Server` accepts connections from a listener.
4. **Handler:** the server calls `ServeHTTP` with the request and a `ResponseWriter`.
5. **Response:** the handler writes a status, headers, and body back to the client.

> These are cooperating components, not an inheritance hierarchy.

*Sources: [net/http documentation](https://pkg.go.dev/net/http)*

<!--
SPEAKER NOTES
Adjacent packages include net/http/httptest, httputil, httptrace, cookiejar and pprof. Routers plug into the Handler interface; they are not tied to a protocol version.
SOURCE LINKS
net/http documentation - https://pkg.go.dev/net/http
-->

---
**2012 ONWARD | THE STANDARD LIBRARY**

# The Handler is the hinge

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}

type HandlerFunc func(ResponseWriter, *Request)

func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r)
}
```

- Any value with `ServeHTTP` can serve a request.
- `HandlerFunc` lets an ordinary function satisfy the interface.

*Source: [Go net/http/server.go](https://go.dev/src/net/http/server.go)*

<!-- SPEAKER NOTES
These definitions are short excerpts from Go's standard library. The implementation is stable, but consult the linked source for your Go version. Example handlers and tests are in examples/.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-2.png)

<!-- SPEAKER NOTES
Timeline stop 2: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**CONCURRENCY | INSIDE NET/HTTP**

# Where does the goroutine start?

```go
// Excerpt from net/http.Server.Serve:
c := s.newConn(rw)
c.setState(c.rwc, StateNew, runHooks)
go c.serve(connCtx)
```

- The listener accepts a connection; `Serve` starts its service goroutine.
- HTTP/1 requests on a connection are handled in sequence; HTTP/2 supports concurrent streams.
- These are implementation details to inspect, not an API promise about goroutine counts.

*Source: [net/http server source](https://go.dev/src/net/http/server.go)*

---

**CONCURRENCY | CHANNELS**

# A worker sends a result to the handler

```go
result := make(chan string, 1)
go func(ctx context.Context) {
    if fetchAndStore(ctx, "example") != nil { return }
    select {
    case result <- "work complete":
    case <-ctx.Done():
    }
}(r.Context())
```

- The handler receives the result and writes the response.
- The worker checks cancellation; it never writes to `ResponseWriter`.

*Source: [Go pipelines and cancellation](https://go.dev/blog/pipelines)*

---
<!-- _class: video -->

# Goroutines and channels

<video controls preload="metadata" playsinline src="videos/channels.mp4"></video>

<!-- SPEAKER NOTES
Silent recording of the runnable demo; use the video controls and narrate live. Source and recording scripts are in demos/ and examples/.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-3.png)

<!-- SPEAKER NOTES
Timeline stop 3: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**2015-2016 | GO 1.6**

# HTTP/2 arrives without a new Handler

**TRANSPARENT PROTOCOL SUPPORT**

- Go 1.6 (February 2016) enables HTTP/2 by default for suitable HTTPS clients and servers.
- TLS ALPN negotiates h2, otherwise HTTP/1.x remains available.
- Detailed HTTP/2 settings initially live in golang.org/x/net/http2.

> Application code stays on Request and ResponseWriter.

*Sources: [Go 1.6 release notes](https://go.dev/doc/go1.6) | [HTTP/2 standard library migration proposal (Jun 2023)](https://github.com/golang/go/discussions/60746)*

<!--
SPEAKER NOTES
Historical implementation detail: x/net/http2 was vendored into net/http via a generated h2_bundle.go. That technical debt later motivated the 2023-2026 migration.
SOURCE LINKS
Go 1.6 release notes - https://go.dev/doc/go1.6
HTTP/2 standard library migration proposal (Jun 2023) - https://github.com/golang/go/discussions/60746
-->

---

**2016 | HTTP/2**

# Multiplexed streams are not URL routing

**HTTP/1.1:** concurrent requests generally use multiple connections; one active exchange per connection.

**HTTP/2:** independent streams can share a single connection.

- HTTP/1.1: at most one active request-response exchange per connection.
- HTTP/2: many streams share a single connection, with flow control and frames.
- Both invoke ordinary net/http handlers.

*Sources: [Go 1.6 release notes](https://go.dev/doc/go1.6) | [net/http documentation](https://pkg.go.dev/net/http)*

<!--
SPEAKER NOTES
The diagram is conceptual. HTTP/1.1 clients can use multiple pooled connections. HTTP/2 multiplexing of frames is a transport concern, while ServeMux dispatches HTTP requests by method, host and path.
SOURCE LINKS
Go 1.6 release notes - https://go.dev/doc/go1.6
net/http documentation - https://pkg.go.dev/net/http
-->

---
<!-- _class: video -->

# Negotiating HTTP/2

<video controls preload="metadata" playsinline src="videos/http2.mp4"></video>

<!-- SPEAKER NOTES
Silent recording of the runnable demo; use the video controls and narrate live. Source and recording scripts are in demos/ and examples/.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-4.png)

<!-- SPEAKER NOTES
Timeline stop 4: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**2017 | LIFECYCLE CODE**

# Operate the server explicitly

```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    IdleTimeout:       60 * time.Second,
}
// On process shutdown:
ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()
_ = srv.Shutdown(ctx)
```

- Bound header reads, idle connections and shutdown time.
- Shutdown waits for normal active connections; it is not a substitute for stopping hijacked connections.

*Sources: [Go 1.8 release notes](https://go.dev/doc/go1.8) | [net/http documentation](https://pkg.go.dev/net/http)*

<!--
SPEAKER NOTES

SOURCE LINKS
Go 1.8 release notes - https://go.dev/doc/go1.8
net/http documentation - https://pkg.go.dev/net/http
-->

---
<!-- _paginate: false -->

![bg](timeline/timeline-5.png)

<!-- SPEAKER NOTES
Timeline stop 5: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**SECURITY | THREAT MODEL**

# What net/http guards - and what it cannot

### RESOURCE LIMITS - Headers, bodies, timeouts

MaxHeaderBytes, MaxBytesReader, ReadHeaderTimeout.

### PROTOCOL BOUNDARIES - TLS, proxy rewriting, path parsing

Validate header semantics; safer ReverseProxy.Rewrite.

### BROWSER REQUESTS - CrossOriginProtection

CSRF mitigation, not authorization.

> None of these replaces identity, business authorization or safe endpoint design.

*Sources: [net/http documentation](https://pkg.go.dev/net/http) | [Go 1.20 release notes](https://go.dev/doc/go1.20) (additional references in speaker notes)*

<!--
SPEAKER NOTES
None of these replaces identity, business authorization or safe endpoint design.
SOURCE LINKS
net/http documentation - https://pkg.go.dev/net/http
Go 1.20 release notes - https://go.dev/doc/go1.20
Go 1.25 release notes - https://go.dev/doc/go1.25
Go 1.27 release notes - https://go.dev/doc/go1.27
-->

---
<!-- _class: video -->

# Limiting a request body

<video controls preload="metadata" playsinline src="videos/security.mp4"></video>

<!-- SPEAKER NOTES
Silent recording of the runnable demo; use the video controls and narrate live. Source and recording scripts are in demos/ and examples/.
-->
---
<!-- _paginate: false -->

![bg](timeline/timeline-6.png)

<!-- SPEAKER NOTES
Timeline stop 6: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**2024 | NEW ROUTING SYNTAX**

# A router in the standard library

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /posts/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    fmt.Fprintln(w, id)
})
mux.HandleFunc("POST /posts", createPost)

// GET also matches HEAD. Unsupported methods get 405 + Allow.
// A missing path gets 404.
```

- Method and path belong in the route declaration.
- Wildcard values are available through Request.PathValue.

*Sources: [Routing enhancements, Go blog (13 Feb 2024)](https://go.dev/blog/routing-enhancements) | [Go 1.22 release notes](https://go.dev/doc/go1.22)*

<!--
SPEAKER NOTES

SOURCE LINKS
Routing enhancements, Go blog (13 Feb 2024) - https://go.dev/blog/routing-enhancements
Go 1.22 release notes - https://go.dev/doc/go1.22
-->

---
<!-- _class: video -->

# When routes collide

<video controls preload="metadata" playsinline src="videos/routing.mp4"></video>

<!-- SPEAKER NOTES
Silent recording of the runnable demo; use the video controls and narrate live. Source and recording scripts are in demos/ and examples/.
-->
---

**ROUTER CHOICE**

# ServeMux versus third-party routing

| Option | Best when | Tradeoff |
| --- | --- | --- |
| HandlerFunc only | One endpoint or custom dispatch | Branch manually |
| net/http.ServeMux | Most small or medium APIs | Fewer advanced grouping features |
| chi | Nested routes + middleware groups | Dependency + its own conventions |
| httprouter | Explicit params; performance focus | Different params/handler options |
| gorilla/mux | Host, query, regex matchers | Broader API + dependency |

*Sources: [net/http documentation](https://pkg.go.dev/net/http) | [Routing enhancements, Go blog (13 Feb 2024)](https://go.dev/blog/routing-enhancements) (additional references in speaker notes)*

<!--
SPEAKER NOTES
All can integrate with the standard HTTP server through http.Handler. This is a qualitative interface comparison, not a performance benchmark. Go 1.22 narrowed the routing feature gap but did not eliminate all reasons to use third-party routers.
SOURCE LINKS
net/http documentation - https://pkg.go.dev/net/http
Routing enhancements, Go blog (13 Feb 2024) - https://go.dev/blog/routing-enhancements
chi router docs - https://pkg.go.dev/github.com/go-chi/chi/v5
httprouter docs - https://pkg.go.dev/github.com/julienschmidt/httprouter
gorilla/mux docs - https://pkg.go.dev/github.com/gorilla/mux
-->

---

**TESTING | UNIT LEVEL**

# Start at the Handler boundary

```go
func TestPostRoute(t *testing.T) {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /posts/{id}", showPost)
    req := httptest.NewRequest(http.MethodGet, "/posts/42", nil)
    rec := httptest.NewRecorder()
    mux.ServeHTTP(rec, req)
    res := rec.Result()
    defer res.Body.Close()
    if res.StatusCode != http.StatusOK {
        t.Fatalf("status: %d", res.StatusCode)
    }
}
```

- Fast: no live listener and no TLS setup.
- Assert status, Allow header, route variables and body.

*Sources: [net/http/httptest documentation](https://pkg.go.dev/net/http/httptest) | [Go HTTP tests](https://go.dev/src/net/http/serve_test.go)*

<!--
SPEAKER NOTES
This is a test sketch: showPost is an application-defined HandlerFunc. ResponseRecorder.Result returns a response snapshot and should be called after handler execution.
SOURCE LINKS
net/http/httptest documentation - https://pkg.go.dev/net/http/httptest
Go 1.22 release notes - https://go.dev/doc/go1.22
-->

---
<!-- _paginate: false -->

![bg](timeline/timeline-7.png)

<!-- SPEAKER NOTES
Timeline stop 7: the highlighted milestone is the next section. See research-changelog.md for the underlying release notes and dates.
-->
---

**2025 | GO 1.24**

# HTTP/2 becomes configurable in net/http

**PROTOCOLS + HTTP2CONFIG**

- Server.Protocols and Transport.Protocols select supported protocol families.
- Server.HTTP2 and Transport.HTTP2 expose HTTP/2 tuning directly.
- Unencrypted HTTP/2 is supported with prior knowledge.
- Deprecated HTTP/1 Upgrade: h2c negotiation is not supported by this API.

> Part of the 2023 consolidation proposal finally reaches the public API.

*Sources: [Go 1.24 release notes](https://go.dev/doc/go1.24) | [HTTP/2 standard library migration proposal (Jun 2023)](https://github.com/golang/go/discussions/60746) (additional references in speaker notes)*

<!--
SPEAKER NOTES
Part of the 2023 consolidation proposal finally reaches the public API.
SOURCE LINKS
Go 1.24 release notes - https://go.dev/doc/go1.24
HTTP/2 standard library migration proposal (Jun 2023) - https://github.com/golang/go/discussions/60746
net/http documentation - https://pkg.go.dev/net/http
-->

---

**AUGUST 2026 | GO 1.27**

# The HTTP/2 migration completes

**New source path:** `net/http/internal/http2`; `x/net/http2` retains compatibility APIs.

- net/http/internal/http2 becomes the source of truth for HTTP/2.
- x/net/http2 remains for compatibility; newer Go versions can wrap stdlib behavior.
- New HTTP/2 feature work moves to the standard library.
- Normal clients and handlers continue using net/http.

> A three-year staged migration is completed without a new Handler API.

*Sources: [x/net/http2 README and migration notes](https://pkg.go.dev/golang.org/x/net/http2) | [Go 1.27 HTTP/2 glue source](https://go.dev/src/net/http/http2.go) (additional references in speaker notes)*

<!--
SPEAKER NOTES
A three-year staged migration is completed without a new Handler API.
SOURCE LINKS
x/net/http2 README and migration notes - https://pkg.go.dev/golang.org/x/net/http2
Go 1.27 HTTP/2 glue source - https://go.dev/src/net/http/http2.go
Go 1.27 release notes - https://go.dev/doc/go1.27
-->

---

**TESTING | INTEGRATION LEVEL**

# Then test over the wire

**httptest**

- httptest.NewServer exercises HTTP/1 end-to-end with a local listener.
- httptest.NewTLSServer / EnableHTTP2 test TLS and negotiated HTTP/2.
- Go's own tests run shared client/server cases across protocol modes.
- Go 1.27 adds httptest.NewTestServer for in-memory fake network tests.

> Unit tests catch Handler logic; integration tests catch protocol behavior.

*Sources: [net/http/httptest documentation](https://pkg.go.dev/net/http/httptest) | [Go 1.14 release notes](https://go.dev/doc/go1.14) (additional references in speaker notes)*

<!--
SPEAKER NOTES
Unit tests catch Handler logic; integration tests catch protocol behavior.
SOURCE LINKS
net/http/httptest documentation - https://pkg.go.dev/net/http/httptest
Go 1.14 release notes - https://go.dev/doc/go1.14
net/http clientserver_test.go (repository source) - https://go.dev/src/net/http/clientserver_test.go
Go 1.27 release notes - https://go.dev/doc/go1.27
-->

---
<!-- _class: lead -->

**DEMO**

# Testing the HTTP stack

<!-- SPEAKER NOTES
Run from go-meetup-nethttp/history/examples: go test -race ./.... The demo runner displays the actual source and then runs the test. A recording can be made with demos/record.sh; no video has been embedded yet.
-->
---
**TAKEAWAYS**

# Before trusting an agent's HTTP code

- Check the **Go version**, protocol, and routing semantics.
- Bound request lifetimes and resources; reuse clients and close bodies.
- Test handlers, cancellation, edge cases, and HTTP/2 on the wire.
- Ask for the source: [net/http](https://pkg.go.dev/net/http), [Go release notes](https://go.dev/doc/devel/release), and the runnable demos.

> The API stayed familiar. Its behavior and capabilities evolved.

<!-- SPEAKER NOTES
The research-changelog.md file contains the chronological release notes and links. The examples/ and demos/ directories contain runnable code and scripts.
-->