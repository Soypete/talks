package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os/signal"
	"syscall"
	"time"

	"golang.org/x/sync/errgroup"
)

// A HandlerFunc can be used directly without a router.
func hello(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Allow", "GET")
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	fmt.Fprintln(w, "hello")
}

func showPost(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, r.PathValue("id"))
}

func routes() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNoContent)
	})
	mux.HandleFunc("GET /posts/{id}", showPost)
	mux.HandleFunc("POST /posts", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusCreated)
	})
	mux.HandleFunc("GET /fanout", fanout)
	mux.HandleFunc("GET /channel", channelHandler)
	return mux
}

// Simulates context-aware work. Replace this with a real downstream call.
func fetchAndStore(ctx context.Context, id string) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-time.After(10 * time.Millisecond):
		return nil
	}
}

func fanout(w http.ResponseWriter, r *http.Request) {
	ids := []string{"one", "two", "three", "four", "five"}
	g, ctx := errgroup.WithContext(r.Context())
	g.SetLimit(4)
	for _, id := range ids {
		id := id
		g.Go(func() error { return fetchAndStore(ctx, id) })
	}
	if err := g.Wait(); err != nil {
		http.Error(w, "upstream failed", http.StatusBadGateway)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// channelHandler demonstrates coordination: only the handler writes the response.
func channelHandler(w http.ResponseWriter, r *http.Request) {
	result := make(chan string, 1)
	go func(ctx context.Context) {
		if err := fetchAndStore(ctx, "example"); err != nil {
			return
		}
		select {
		case result <- "work complete":
		case <-ctx.Done():
		}
	}(r.Context())

	select {
	case message := <-result:
		fmt.Fprintln(w, message)
	case <-r.Context().Done():
		return
	}
}

func main() {
	addr := flag.String("addr", ":8080", "listen address")
	direct := flag.Bool("direct", false, "serve a single handler without a router")
	cert := flag.String("cert", "", "TLS certificate (requires -key)")
	key := flag.String("key", "", "TLS private key (requires -cert)")
	flag.Parse()
	if (*cert == "") != (*key == "") {
		log.Fatal("provide both -cert and -key")
	}

	var handler http.Handler = routes()
	if *direct {
		handler = http.HandlerFunc(hello)
	}
	protocols := new(http.Protocols)
	protocols.SetHTTP1(true)
	protocols.SetHTTP2(true)
	srv := &http.Server{
		Addr: *addr, Handler: handler, Protocols: protocols,
		ReadHeaderTimeout: 5 * time.Second, IdleTimeout: 60 * time.Second,
	}
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	done := make(chan error, 1)
	go func() {
		if *cert != "" {
			done <- srv.ListenAndServeTLS(*cert, *key)
			return
		}
		done <- srv.ListenAndServe()
	}()
	log.Printf("listening on %s", *addr)
	select {
	case err := <-done:
		if !errors.Is(err, http.ErrServerClosed) {
			log.Fatal(err)
		}
	case <-ctx.Done():
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()
		if err := srv.Shutdown(shutdownCtx); err != nil {
			log.Fatal(err)
		}
		if err := <-done; !errors.Is(err, http.ErrServerClosed) {
			log.Fatal(err)
		}
	}
}
