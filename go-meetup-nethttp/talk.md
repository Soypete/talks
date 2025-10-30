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

A practical guide to building robust HTTP servers in Go

---

<!-- _class: lead -->

## Who Am I?

**Pete Soloway** (@soypete)
Developer Advocate @ Weaviate
Go enthusiast, conference speaker, workshop instructor

🐦 Twitter/X: @soypete
💼 GitHub: github.com/soypete
📧 pete@weaviate.io

---

## What We'll Cover Today

- Building HTTP servers with net/http
- Request routing patterns and muxes
- Authentication strategies
- Connection pooling and the default client problem
- Testing with httptest

---

<!-- _class: lead -->

# Part 1: Building Servers
## The net/http Package

---

## Why net/http?

The Go standard library provides everything you need:
- HTTP/1.1 and HTTP/2 support
- TLS/SSL built-in
- Middleware patterns
- Context support
- Production-ready performance

No frameworks required for most use cases!

---

## Simple Server Example

```go
package main

import (
    "fmt"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, World!")
}

func main() {
    http.HandleFunc("/hello", helloHandler)
    http.ListenAndServe(":8080", nil)
}
```

---

## Handler Functions

Two ways to handle requests:

**1. HandlerFunc** - Simple function signature
```go
func(w http.ResponseWriter, r *http.Request)
```

**2. Handler Interface** - More flexibility
```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

---

## The Request Object

Key components of `*http.Request`:

- `Method` - HTTP method (GET, POST, PUT, DELETE)
- `URL` - Request URL with path and query params
- `Header` - HTTP headers map
- `Body` - Request body (io.ReadCloser)
- `Context()` - Request context for cancellation/timeouts

---

## The ResponseWriter

`http.ResponseWriter` interface:

- `Header()` - Modify response headers
- `Write([]byte)` - Write response body
- `WriteHeader(int)` - Set HTTP status code

**Important**: Headers must be set before writing body!

---

<!-- _class: lead -->

# Part 2: Request Routing
## Muxes and Patterns

---

## The Default ServeMux

Go provides a default request multiplexer:

```go
http.HandleFunc("/api/users", usersHandler)
http.HandleFunc("/api/posts", postsHandler)
http.ListenAndServe(":8080", nil)
```

Limited pattern matching:
- Exact paths
- Subtree patterns with trailing `/`
- No method routing
- No path parameters

---

## Custom ServeMux

Create your own mux for better control:

```go
mux := http.NewServeMux()
mux.HandleFunc("/api/users", usersHandler)
mux.HandleFunc("/api/posts", postsHandler)

server := &http.Server{
    Addr:    ":8080",
    Handler: mux,
}
server.ListenAndServe()
```

---

## Method-Based Routing

Handle different HTTP methods:

```go
func usersHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        getUsers(w, r)
    case http.MethodPost:
        createUser(w, r)
    case http.MethodPut:
        updateUser(w, r)
    case http.MethodDelete:
        deleteUser(w, r)
    default:
        http.Error(w, "Method not allowed",
                   http.StatusMethodNotAllowed)
    }
}
```

---

## Popular Third-Party Routers

When you need more features:

- **gorilla/mux** - Path variables, method routing
- **chi** - Lightweight, composable
- **httprouter** - High performance, zero allocation
- **gin** - Full framework with routing

Consider: Do you need the complexity?

---

<!-- _class: lead -->

# Part 3: Authentication
## Securing Your Services

---

## Authentication Types

Common patterns in HTTP services:

1. **Basic Auth** - Username/password (base64)
2. **Bearer Tokens** - JWT, OAuth tokens
3. **API Keys** - Custom header or query param
4. **OAuth 2.0** - Third-party authorization

---

## Basic Authentication

Built into net/http:

```go
func basicAuthHandler(w http.ResponseWriter, r *http.Request) {
    username, password, ok := r.BasicAuth()
    if !ok {
        w.Header().Set("WWW-Authenticate",
                       `Basic realm="restricted"`)
        http.Error(w, "Unauthorized",
                   http.StatusUnauthorized)
        return
    }

    if !validCredentials(username, password) {
        http.Error(w, "Forbidden", http.StatusForbidden)
        return
    }

    // Continue with authenticated request
}
```

---

## Bearer Token Authentication

Common for APIs:

```go
func bearerAuthHandler(w http.ResponseWriter, r *http.Request) {
    authHeader := r.Header.Get("Authorization")
    if authHeader == "" {
        http.Error(w, "Missing auth token",
                   http.StatusUnauthorized)
        return
    }

    token := strings.TrimPrefix(authHeader, "Bearer ")
    if !validateToken(token) {
        http.Error(w, "Invalid token",
                   http.StatusForbidden)
        return
    }

    // Process authenticated request
}
```

---

## Authentication Middleware

DRY principle - wrap handlers:

```go
func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if !validateToken(token) {
            http.Error(w, "Unauthorized",
                       http.StatusUnauthorized)
            return
        }
        next(w, r)
    }
}

// Usage
http.HandleFunc("/api/protected",
                authMiddleware(protectedHandler))
```

---

<!-- _class: lead -->

# Part 4: The Default Client Problem
## Connection Pooling and Configuration

---

## The Default Client Issue

```go
// DON'T do this in production!
resp, err := http.Get("https://api.example.com/data")
```

Problems:
- No timeout (hangs forever)
- Uncontrolled connection pooling
- No retry logic
- Difficult to customize

---

## Connection Pooling Basics

HTTP keep-alive reuses TCP connections:

- Reduces latency
- Saves CPU and memory
- But needs limits!

Default pool limits may not suit your needs:
- MaxIdleConns: 100
- MaxIdleConnsPerHost: 2 (usually too low!)
- IdleConnTimeout: 90 seconds

---

## Creating a Custom Client

```go
var httpClient = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
        DisableKeepAlives:   false,
        DisableCompression:  false,
    },
}

// Use it everywhere
resp, err := httpClient.Get("https://api.example.com/data")
```

---

## Important Transport Settings

```go
&http.Transport{
    // Connection pooling
    MaxIdleConns:        100,    // Total idle connections
    MaxIdleConnsPerHost: 10,     // Per-host idle connections
    MaxConnsPerHost:     0,      // Unlimited (0)

    // Timeouts
    IdleConnTimeout:       90 * time.Second,
    ResponseHeaderTimeout: 10 * time.Second,
    ExpectContinueTimeout: 1 * time.Second,

    // TLS
    TLSHandshakeTimeout: 10 * time.Second,
}
```

---

## Client Timeouts

Multiple timeout types:

```go
client := &http.Client{
    Timeout: 30 * time.Second, // Overall request timeout
    Transport: &http.Transport{
        DialContext: (&net.Dialer{
            Timeout:   5 * time.Second,  // Connection timeout
            KeepAlive: 30 * time.Second,
        }).DialContext,
        TLSHandshakeTimeout:   10 * time.Second,
        ResponseHeaderTimeout: 10 * time.Second,
    },
}
```

---

## Connection Pool Best Practices

1. **Create one client per host/service**
   - Reuse clients across requests
   - Don't create new clients per request

2. **Tune MaxIdleConnsPerHost**
   - Default of 2 is usually too low
   - Set to match expected concurrent requests

3. **Set appropriate timeouts**
   - Prevent hanging requests
   - Account for slow networks

---

<!-- _class: lead -->

# Part 5: Testing
## httptest Package

---

## Why httptest?

Testing HTTP services should be:
- Fast (no real network calls)
- Reliable (no external dependencies)
- Isolated (test one component)

`net/http/httptest` provides:
- Mock servers
- Response recorders
- Request builders

---

## ResponseRecorder

Test handlers without a server:

```go
func TestHelloHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/hello", nil)
    w := httptest.NewRecorder()

    helloHandler(w, req)

    resp := w.Result()
    body, _ := io.ReadAll(resp.Body)

    if resp.StatusCode != http.StatusOK {
        t.Errorf("Expected 200, got %d", resp.StatusCode)
    }
    if string(body) != "Hello, World!" {
        t.Errorf("Unexpected body: %s", body)
    }
}
```

---

## Test Server

Test HTTP clients:

```go
func TestAPIClient(t *testing.T) {
    server := httptest.NewServer(
        http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            w.WriteHeader(http.StatusOK)
            w.Write([]byte(`{"status":"ok"}`))
        }),
    )
    defer server.Close()

    client := NewAPIClient(server.URL)
    status, err := client.GetStatus()

    if err != nil {
        t.Fatalf("Unexpected error: %v", err)
    }
    if status != "ok" {
        t.Errorf("Expected status ok, got %s", status)
    }
}
```

---

## Testing with Table Tests

Go idiom for comprehensive testing:

```go
func TestUserHandler(t *testing.T) {
    tests := []struct {
        name           string
        method         string
        body           string
        expectedStatus int
        expectedBody   string
    }{
        {"valid GET", "GET", "", 200, `{"users":[]}`},
        {"invalid POST", "POST", "invalid", 400, ""},
        {"unauthorized", "DELETE", "", 401, ""},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Test logic here
        })
    }
}
```

---

## Testing Middleware

Test middleware in isolation:

```go
func TestAuthMiddleware(t *testing.T) {
    nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("success"))
    })

    handlerToTest := authMiddleware(nextHandler)

    req := httptest.NewRequest("GET", "/", nil)
    req.Header.Set("Authorization", "Bearer valid-token")
    w := httptest.NewRecorder()

    handlerToTest(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("Expected 200, got %d", w.Code)
    }
}
```

---

<!-- _class: lead -->

# Key Takeaways

---

## Remember

1. **net/http is powerful** - You don't always need a framework
2. **Routing matters** - Choose the right mux for your needs
3. **Secure early** - Implement auth from the start
4. **Customize the client** - Don't use http.Get in production
5. **Test everything** - httptest makes it easy

---

<!-- _class: lead -->

# Questions?

---

## Resources

- Go net/http docs: https://pkg.go.dev/net/http
- Go net/http/httptest: https://pkg.go.dev/net/http/httptest
- Workshop materials: github.com/Soypete/Webservices-in-3-weeks
- Effective Go: https://go.dev/doc/effective_go

**Slides**: github.com/soypete/talks

**Contact**: @soypete | pete@weaviate.io
