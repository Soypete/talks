# net/http Examples

Runnable examples from the "Beyond Hello World" talk.

## Running Examples

Each example is in its own directory. To run:

```bash
cd 01-simple-server
go run main.go
```

## Examples

### 01-simple-server
Basic HTTP server with a single handler.

```bash
curl http://localhost:8080/hello
```

### 02-routing-122
Go 1.22+ routing with method-based routing and path parameters.

```bash
curl http://localhost:8080/users/123
curl -X POST http://localhost:8080/users
curl -X DELETE http://localhost:8080/users/123
```

### 03-middleware
Logging and authentication middleware with chaining.

```bash
curl http://localhost:8080/public
curl http://localhost:8080/protected
curl -H 'Authorization: Bearer secret-token' http://localhost:8080/protected
```

### 04-fileserver
Static file serving with `http.FileServer` and `http.StripPrefix`.

```bash
# Visit in browser
open http://localhost:8080/static/
open http://localhost:8080/static/index.html
```

### 05-graceful-shutdown
Graceful server shutdown with `Server.Shutdown()`.

```bash
# Press Ctrl+C to trigger graceful shutdown
# Try making a request while shutting down to see it complete
```

## More Examples

For comprehensive examples including databases, testing, and production patterns, see:

**WebServices in 3 Weeks Workshop**: https://github.com/Soypete/WebServices-in-3-weeks
