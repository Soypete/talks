package main

import (
	"fmt"
	"log"
	"net/http"
)

func getUserHandler(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	fmt.Fprintf(w, "Getting user: %s\n", id)
}

func createUserHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Creating new user\n")
}

func deleteUserHandler(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	fmt.Fprintf(w, "Deleting user: %s\n", id)
}

func main() {
	mux := http.NewServeMux()

	// Go 1.22+ method and path parameter routing
	mux.HandleFunc("GET /users/{id}", getUserHandler)
	mux.HandleFunc("POST /users", createUserHandler)
	mux.HandleFunc("DELETE /users/{id}", deleteUserHandler)

	log.Println("Server starting on :8080")
	log.Println("Try: curl http://localhost:8080/users/123")
	log.Println("Try: curl -X POST http://localhost:8080/users")
	log.Println("Try: curl -X DELETE http://localhost:8080/users/123")

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
