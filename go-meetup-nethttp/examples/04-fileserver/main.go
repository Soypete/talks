package main

import (
	"log"
	"net/http"
	"os"
)

func main() {
	// Create a sample static directory with a file
	os.MkdirAll("static/css", 0755)
	os.WriteFile("static/index.html", []byte("<h1>Hello from FileServer!</h1>"), 0644)
	os.WriteFile("static/css/style.css", []byte("body { color: blue; }"), 0644)

	mux := http.NewServeMux()

	// Serve static files with StripPrefix
	fs := http.FileServer(http.Dir("./static"))
	mux.Handle("/static/", http.StripPrefix("/static/", fs))

	log.Println("Server starting on :8080")
	log.Println("Try: http://localhost:8080/static/")
	log.Println("Try: http://localhost:8080/static/index.html")
	log.Println("Try: http://localhost:8080/static/css/style.css")

	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
