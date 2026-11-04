# net/http release-by-release research journal (as of 26 October 2026)

Scope: chronology of substantive HTTP-related standard-library changes; **not** an exhaustive commit-level log. Separate HTTP protocol versions from Go release numbers. Every item below links to the primary source.

## 2009

Go is publicly announced; networking and HTTP evolve before the Go 1 API freeze.

Source: [Go 1 announcement, 28 Mar 2012](https://go.dev/blog/go1)

## 2012-03 | Go 1

The package path changes from http to net/http; specialized functions move to httputil. Go 1 compatibility promise.

Source: [Go 1 release notes](https://go.dev/doc/go1)

## 2014-07

The Go team publishes request-context concurrency patterns; handlers serve each request in a goroutine.

Source: [Go Concurrency Patterns: Context (2014)](https://go.dev/blog/context)

## 2016-02 | Go 1.6

Transparent HTTPS HTTP/2 clients/servers; x/net/http2 provides optional advanced configuration.

Source: [Go 1.6 release notes](https://go.dev/doc/go1.6)

## 2016-08 | Go 1.7

Request.Context and WithContext; transport dial context, idle pool and response-header limits.

Source: [Go 1.7 release notes](https://go.dev/doc/go1.7)

## 2017-02 | Go 1.8

Graceful Server.Shutdown; ReadHeaderTimeout and IdleTimeout; request context cancellation on connection close.

Source: [Go 1.8 release notes](https://go.dev/doc/go1.8)

## 2018-08 | Go 1.11

Transport.MaxConnsPerHost and cookie SameSite support.

Source: [Go 1.11 release notes](https://go.dev/doc/go1.11)

## 2019-09 | Go 1.13

Transport.ForceAttemptHTTP2 and read/write buffer sizing.

Source: [Go 1.13 release notes](https://go.dev/doc/go1.13)

## 2020-02 | Go 1.14

httptest.Server.EnableHTTP2 and context-aware TLS dial support.

Source: [Go 1.14 release notes](https://go.dev/doc/go1.14)

## 2021-02 | Go 1.16

http.FS integration with io/fs.

Source: [Go 1.16 release notes](https://go.dev/doc/go1.16)

## 2021-08 | Go 1.17

Context-aware TLS handshakes and stricter Host handling.

Source: [Go 1.17 release notes](https://go.dev/doc/go1.17)

## 2022-03 | Go 1.18

Fuzzing integrated into Go tooling; important for protocol parser testing.

Source: [Go 1.18 release notes](https://go.dev/doc/go1.18)

## 2022-08 | Go 1.19

User-defined 1xx headers and MaxBytesError; memory model revisions.

Source: [Go 1.19 release notes](https://go.dev/doc/go1.19)

## 2022-12 | security

HTTP/2 header-cache memory growth vulnerability (GO-2022-1144) fixed in maintained releases.

Source: [GO-2022-1144: HTTP/2 header memory](https://pkg.go.dev/vuln/GO-2022-1144)

## 2023-02 | Go 1.20

ResponseController for per-request capabilities; ReverseProxy.Rewrite addresses Director issue.

Source: [Go 1.20 release notes](https://go.dev/doc/go1.20)

## 2023-06 | proposal

HTTP/2 move from x/net/http2 to internal stdlib package proposed; bundle generation and testing complexity cited.

Source: [HTTP/2 standard library migration proposal (Jun 2023)](https://github.com/golang/go/discussions/60746)

## 2023-07 | proposal

New ServeMux proposal for method-specific and wildcard routes.

Source: [ServeMux proposal #61410 (Jul 2023)](https://github.com/golang/go/issues/61410)

## 2023-08 | Go 1.21

ResponseController.EnableFullDuplex (HTTP/1 request/response concurrency).

Source: [Go 1.21 release notes](https://go.dev/doc/go1.21)

## 2024-02 | Go 1.22

Method-aware ServeMux + wildcards, PathValue and SetPathValue; GODEBUG=httpmuxgo121.

Source: [Go 1.22 release notes](https://go.dev/doc/go1.22)

## 2024-08 | Go 1.23

Request.Pattern, httptest.NewRequestWithContext and expanded Cookie APIs.

Source: [Go 1.23 release notes](https://go.dev/doc/go1.23)

## 2025-02 | Go 1.24

Server/Transport.Protocols and HTTP2 fields; cleartext HTTP/2 prior knowledge, not Upgrade:h2c.

Source: [Go 1.24 release notes](https://go.dev/doc/go1.24)

## 2025-08 | Go 1.25

CrossOriginProtection; testing/synctest stable (tooling).

Source: [Go 1.25 release notes](https://go.dev/doc/go1.25)

## 2026-02 | Go 1.26

NewClientConn, StrictMaxConcurrentRequests, ReverseProxy.Director deprecation, ServeMux 307 slash redirects.

Source: [Go 1.26 release notes](https://go.dev/doc/go1.26)

## 2026-08 | Go 1.27

HTTP/2 source moves to net/http/internal/http2, x/net compatibility wrapper. HTTP/2 client priority, HTTP/1 response-draining, header-count limit, httptest.NewTestServer, goroutine leak profile.

Source: [Go 1.27 release notes](https://go.dev/doc/go1.27)

## 2026-10 | security

GO-2026-6610 / GO-2026-6613 fixed in Go 1.26.9 and 1.27.2 (8 Oct); 1.27.3 shipped 19 Oct for other security.

Source: [Go release history](https://go.dev/doc/devel/release)

## Primary technical references

- [Go release history](https://go.dev/doc/devel/release)
- [Go 1 announcement, 28 Mar 2012](https://go.dev/blog/go1)
- [Go 1 release notes](https://go.dev/doc/go1)
- [net/http documentation](https://pkg.go.dev/net/http)
- [net/http/httptest documentation](https://pkg.go.dev/net/http/httptest)
- [Go 1.6 release notes](https://go.dev/doc/go1.6)
- [Go 1.7 release notes](https://go.dev/doc/go1.7)
- [Go 1.8 release notes](https://go.dev/doc/go1.8)
- [Go 1.11 release notes](https://go.dev/doc/go1.11)
- [Go 1.13 release notes](https://go.dev/doc/go1.13)
- [Go 1.14 release notes](https://go.dev/doc/go1.14)
- [Go 1.16 release notes](https://go.dev/doc/go1.16)
- [Go 1.17 release notes](https://go.dev/doc/go1.17)
- [Go 1.18 release notes](https://go.dev/doc/go1.18)
- [Go 1.19 release notes](https://go.dev/doc/go1.19)
- [Go 1.20 release notes](https://go.dev/doc/go1.20)
- [Go 1.21 release notes](https://go.dev/doc/go1.21)
- [Go 1.22 release notes](https://go.dev/doc/go1.22)
- [Go 1.23 release notes](https://go.dev/doc/go1.23)
- [Go 1.24 release notes](https://go.dev/doc/go1.24)
- [Go 1.25 release notes](https://go.dev/doc/go1.25)
- [Go 1.26 release notes](https://go.dev/doc/go1.26)
- [Go 1.27 release notes](https://go.dev/doc/go1.27)
- [HTTP/2 standard library migration proposal (Jun 2023)](https://github.com/golang/go/discussions/60746)
- [x/net/http2 README and migration notes](https://pkg.go.dev/golang.org/x/net/http2)
- [Go 1.27 HTTP/2 glue source](https://go.dev/src/net/http/http2.go)
- [Routing enhancements, Go blog (13 Feb 2024)](https://go.dev/blog/routing-enhancements)
- [ServeMux proposal #61410 (Jul 2023)](https://github.com/golang/go/issues/61410)
- [Legacy 1.21 ServeMux snapshot](https://go.dev/src/net/http/servemux121.go)
- [Go Concurrency Patterns: Context (2014)](https://go.dev/blog/context)
- [Testing Time (and other asynchronicities), 2025](https://go.dev/blog/testing-time)
- [net/http clientserver_test.go (repository source)](https://go.dev/src/net/http/clientserver_test.go)
- [net/http serve_test.go (repository source)](https://go.dev/src/net/http/serve_test.go)
- [Go fuzzing guide](https://go.dev/doc/security/fuzz/)
- [gorilla/mux docs](https://pkg.go.dev/github.com/gorilla/mux)
- [chi router docs](https://pkg.go.dev/github.com/go-chi/chi/v5)
- [httprouter docs](https://pkg.go.dev/github.com/julienschmidt/httprouter)
- [net/http CrossOriginProtection API](https://pkg.go.dev/net/http#CrossOriginProtection)
- [GO-2022-1144: HTTP/2 header memory](https://pkg.go.dev/vuln/GO-2022-1144)
- [GO-2026-6610: HTTP/2 header handling](https://pkg.go.dev/vuln/GO-2026-6610)
- [GO-2026-6613: CONNECT request smuggling](https://pkg.go.dev/vuln/GO-2026-6613)
- [Better HTTP/1 connection reuse, 14 Oct 2026](https://go.dev/blog/http-connection-reuse)
- [Goroutine Leak Profiles, Sep 2026](https://go.dev/blog/goroutine-leak-profiles)

## Interpretation of the 2022 migration memory

The documented HTTP/2 source-of-truth move was **proposed June 12, 2023** and **completed in Go 1.27 (August 2026)**. The routing rework was **proposed July 2023**, shipped in **Go 1.22 (February 2024)**. The year 2022 marked significant testing/security changes but should not be shown as the date either migration landed. The historical `http` -> `net/http` path change was Go 1.0 in 2012.
