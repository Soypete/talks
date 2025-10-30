---
marp: true
theme: gaia
paginate: true
title: "Beyond Hello World: Mastering net/http for Production Go Services"
backgroundImage: url('../images/soypete_background.png')
description: A deep dive into Go's net/http package covering servers, auth, routing, connection pooling, and testing strategies
---

<!-- _class: lead -->

# Beyond Hello World
## Mastering net/http for Production Go Services

---

## Who Am I?

**Miriah Peterson**
Data Engineer at SchoolAI
Organizer: GoWest, Forge Utah
SoyPeteTech: Substack, Twitch, YouTube
O'Reilly Go Course Instructor

---

## What We'll Cover

- Servers, handlers, and constants
- HTTP/1 vs HTTP/2
- TLS and graceful shutdown
- FileServer and less common types
- Auth, routing, and connection pools
- Testing with httptest

---

<!-- _class: lead -->

# Part 1: Building Servers

---

## Simple Server

```go
func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, World!")
}

func main() {
    http.HandleFunc("/hello", helloHandler)
    http.ListenAndServe(":8080", nil)
}
```

---

## Handler Types

**HandlerFunc** - Simple function
```go
func(w http.ResponseWriter, r *http.Request)
```

**Handler Interface** - More control
```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

---

## http.Request Essentials

- `Method` - GET, POST, PUT, DELETE
- `URL` - Path and query params
- `Header` - HTTP headers
- `Body` - Request body (io.ReadCloser)
- `Context()` - Cancellation/timeouts
- `BasicAuth()` - Built-in basic auth helper

---

## http.ResponseWriter

Three key methods:
- `Header()` - Modify response headers
- `Write([]byte)` - Write response body
- `WriteHeader(int)` - Set status code

**Headers must be set before writing body!**

---

## Constants Are Your Friends

Use stdlib constants for readability:
```go
http.StatusOK                    // 200
http.StatusNotFound              // 404
http.MethodGet, http.MethodPost  // "GET", "POST"
```

**See all constants**: https://pkg.go.dev/net/http#pkg-constants

---

<!-- _class: lead -->

# FileServer & Less Common Types

---

## http.FileServer

Serve static files easily:
```go
fs := http.FileServer(http.Dir("./static"))
http.Handle("/static/", http.StripPrefix("/static/", fs))
```

Example: https://pkg.go.dev/net/http#example-FileServer

---

## StripPrefix

Remove path prefix before serving:
```go
handler := http.StripPrefix("/static/",
    http.FileServer(http.Dir("./assets")))
http.Handle("/static/", handler)
```

Request `/static/css/style.css` → serves `./assets/css/style.css`

---

## NotFoundHandler

Custom 404 responses:
```go
notFound := http.NotFoundHandler()
http.Handle("/old-path", notFound)
```

Or create your own custom handler!

---

## Hijacker Interface

Take over the connection (WebSockets, etc):
```go
type Hijacker interface {
    Hijack() (net.Conn, *bufio.ReadWriter, error)
}
```

Advanced use case - raw TCP control

---

<!-- _class: lead -->

# HTTP/1 vs HTTP/2

---

## Protocol Support

HTTP/2 enabled by default:
```go
server := &http.Server{
    Addr:    ":8080",
    Handler: handler,
}
server.ListenAndServe()  // Supports both HTTP/1.1 and HTTP/2
```

Example: https://pkg.go.dev/net/http#example-package-Http2

---

## Force HTTP/1 Only

```go
server := &http.Server{
    Addr:    ":8080",
    Handler: handler,
    TLSNextProto: make(map[string]func(*http.Server,
                        *tls.Conn, http.Handler)),
}
```

Usually not needed - HTTP/2 is faster!

---

<!-- _class: lead -->

# TLS/HTTPS

---

## ListenAndServeTLS

```go
func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServeTLS(":443",
        "cert.pem",
        "key.pem",
        nil)
}
```

That's it - HTTPS enabled!

---

## Custom TLS Config

```go
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS13,
    CipherSuites: []uint16{tls.TLS_AES_256_GCM_SHA384},
}
server := &http.Server{
    Addr:      ":443",
    TLSConfig: tlsConfig,
}
server.ListenAndServeTLS("cert.pem", "key.pem")
```

---

<!-- _class: lead -->

# Graceful Shutdown

---

## Server.Shutdown

```go
server := &http.Server{Addr: ":8080", Handler: handler}

go server.ListenAndServe()

// Wait for interrupt signal
<-ctx.Done()

shutdownCtx, cancel := context.WithTimeout(
    context.Background(), 5*time.Second)
defer cancel()

server.Shutdown(shutdownCtx)
```

---

<!-- _class: lead -->

# Request Routing

---

## Default ServeMux

```go
http.HandleFunc("/api/users", usersHandler)
http.ListenAndServe(":8080", nil)
```

Limited features:
- Exact paths or subtree `/`
- No method routing
- No path parameters

---

## Custom ServeMux

```go
mux := http.NewServeMux()
mux.HandleFunc("/api/users", usersHandler)
server := &http.Server{Addr: ":8080", Handler: mux}
server.ListenAndServe()
```

Better control and isolation

---

## Method-Based Routing

```go
func handler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        handleGet(w, r)
    case http.MethodPost:
        handlePost(w, r)
    default:
        http.Error(w, "Method not allowed", 405)
    }
}
```

---

<!-- _class: lead -->

# Authentication

---

## Auth Strategies

1. **Basic Auth** - Base64 username:password
2. **Bearer Tokens** - JWT, OAuth
3. **API Keys** - Custom headers
4. **OAuth 2.0** - Third-party auth

---

## Basic Auth

Built-in helper:
```go
username, password, ok := r.BasicAuth()
if !ok || !valid(username, password) {
    w.Header().Set("WWW-Authenticate", `Basic realm="api"`)
    http.Error(w, "Unauthorized", 401)
    return
}
```

---

## Auth Middleware

```go
func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if !validateToken(r.Header.Get("Authorization")) {
            http.Error(w, "Unauthorized", 401)
            return
        }
        next(w, r)
    }
}
```

---

<!-- _class: lead -->

# The Default Client Problem

---

## Don't Use http.Get!

```go
// BAD - No timeout!
resp, err := http.Get("https://api.example.com")
```

Problems: No timeout, poor pooling defaults

---

## Create Custom Client

```go
var client = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConnsPerHost: 10,  // Default is 2!
        IdleConnTimeout:     90 * time.Second,
    },
}
```

**Reuse this client everywhere**

---

## Connection Pooling

Key settings:
- `MaxIdleConns: 100` - Total pool size
- `MaxIdleConnsPerHost: 10` - Per-host limit
- `IdleConnTimeout: 90s` - Idle timeout

Default `MaxIdleConnsPerHost` of 2 is too low!

---

<!-- _class: lead -->

# Testing with httptest

---

## httptest.ResponseRecorder

Test handlers directly:
```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/hello", nil)
    w := httptest.NewRecorder()
    helloHandler(w, req)

    if w.Code != 200 {
        t.Errorf("Got %d", w.Code)
    }
}
```

---

## httptest.NewServer

Test HTTP clients:
```go
server := httptest.NewServer(http.HandlerFunc(
    func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte(`{"status":"ok"}`))
    }))
defer server.Close()

client := NewAPIClient(server.URL)
```

---

## Table Tests

```go
tests := []struct {
    name   string
    method string
    want   int
}{
    {"GET", "GET", 200},
    {"DELETE", "DELETE", 401},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { /*...*/ })
}
```

---

<!-- _class: lead -->

# Key Takeaways

---

## Remember

- Use stdlib constants for readability
- HTTP/2 is enabled by default
- Always use custom clients, never `http.Get`
- Graceful shutdown with `Server.Shutdown()`
- TLS is just `ListenAndServeTLS()`
- `httptest` makes testing easy

---

<!-- _class: lead -->

# Questions?

---

## Resources

**Examples**: https://pkg.go.dev/net/http#pkg-examples
**Constants**: https://pkg.go.dev/net/http#pkg-constants
**Workshop**: github.com/Soypete/Webservices-in-3-weeks

**Slides**: github.com/soypete/talks
**Contact**: SoyPeteTech on Substack, Twitch, YouTube
