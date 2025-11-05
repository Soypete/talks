package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

// Logging middleware
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		log.Printf("Started %s %s", r.Method, r.URL.Path)

		next.ServeHTTP(w, r)

		log.Printf("Completed in %v", time.Since(start))
	})
}

// Auth middleware
func authMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")
		if token != "Bearer secret-token" {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func protectedHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "You accessed the protected resource!\n")
}

func publicHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "This is a public resource\n")
}

func main() {
	mux := http.NewServeMux()

	// Public route with only logging
	mux.Handle("/public", loggingMiddleware(http.HandlerFunc(publicHandler)))

	// Protected route with both logging and auth
	mux.Handle("/protected",
		loggingMiddleware(
			authMiddleware(http.HandlerFunc(protectedHandler))))

	log.Println("Server starting on :8080")
	log.Println("Try: curl http://localhost:8080/public")
	log.Println("Try: curl http://localhost:8080/protected")
	log.Println("Try: curl -H 'Authorization: Bearer secret-token' http://localhost:8080/protected")

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
