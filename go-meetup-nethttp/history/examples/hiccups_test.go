package main

import (
	"context"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// Registering overlapping patterns without a more-specific winner panics at startup.
func TestDemoRouteConflict(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Fatal("expected conflicting patterns to panic")
		}
		t.Log("conflicting route patterns rejected at registration")
	}()
	mux := http.NewServeMux()
	mux.HandleFunc("GET /posts/{id}", showPost)
	mux.HandleFunc("GET /{resource}/latest", showPost)
}

func TestDemoBodyLimit(t *testing.T) {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		r.Body = http.MaxBytesReader(w, r.Body, 4)
		_, err := io.ReadAll(r.Body)
		var limit *http.MaxBytesError
		if errors.As(err, &limit) {
			http.Error(w, "body too large", http.StatusRequestEntityTooLarge)
			return
		}
		if err != nil {
			http.Error(w, "bad body", http.StatusBadRequest)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	})
	for _, tc := range []struct {
		body string
		want int
	}{{"1234", 204}, {"12345", 413}} {
		rec := httptest.NewRecorder()
		handler.ServeHTTP(rec, httptest.NewRequest("POST", "/", strings.NewReader(tc.body)))
		if rec.Code != tc.want {
			t.Fatalf("body %q: got %d want %d", tc.body, rec.Code, tc.want)
		}
		t.Logf("%d bytes -> %d", len(tc.body), rec.Code)
	}
}

func TestDemoContextCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if err := fetchAndStore(ctx, "post"); !errors.Is(err, context.Canceled) {
		t.Fatalf("got %v", err)
	}
	t.Log("child work returned context.Canceled")
}

func TestDemoClientTimeout(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		<-r.Context().Done()
	}))
	defer ts.Close()
	client := &http.Client{Timeout: 20 * time.Millisecond}
	res, err := client.Get(ts.URL)
	if res != nil {
		res.Body.Close()
	}
	if err == nil || !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("expected deadline error, got %v", err)
	}
	t.Log("client timeout canceled the request")
}
