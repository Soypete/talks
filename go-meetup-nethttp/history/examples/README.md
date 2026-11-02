# Runnable slide examples

Requires Go 1.24 or later and the `golang.org/x/sync` module (downloaded on first run). The fake-time test also requires Go 1.27; it is automatically skipped on earlier versions.

```sh
cd go-meetup-nethttp/history/examples
go run .
```

In another terminal:

```sh
curl -i localhost:8080/health
curl -i localhost:8080/posts/42
curl -i -X POST localhost:8080/posts
curl -i localhost:8080/fanout
curl -i -X PUT localhost:8080/posts/42
```

Stop the server with Ctrl+C to exercise graceful shutdown. Run `go run . -direct` to serve a single handler without a router. For TLS and HTTP/2, pass a certificate and key with `go run . -cert cert.pem -key key.pem`; `go test` negotiates HTTP/2 automatically with an ephemeral test certificate.

```sh
go test -race ./...
```

`main.go` brings together the slides' health handler, ServeMux routes, protocol configuration, direct handler, bounded fan-out and shutdown. `main_test.go` exercises routing and HTTP/2 over a local listener. `synctest_test.go` runs the Go 1.27 fake-time example using an in-memory network.
