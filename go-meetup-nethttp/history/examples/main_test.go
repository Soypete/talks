package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestPostRoute(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/posts/42", nil)
	rec := httptest.NewRecorder()
	routes().ServeHTTP(rec, req)
	res := rec.Result()
	defer res.Body.Close()
	body, err := io.ReadAll(res.Body)
	if err != nil {
		t.Fatal(err)
	}
	if res.StatusCode != http.StatusOK || string(body) != "42\n" {
		t.Fatalf("status %d, body %q", res.StatusCode, body)
	}
}

func TestMethodsAndFanout(t *testing.T) {
	for _, tc := range []struct {
		method, path string
		want         int
	}{
		{"HEAD", "/posts/42", http.StatusOK},
		{"PUT", "/posts/42", http.StatusMethodNotAllowed},
		{"POST", "/posts", http.StatusCreated},
		{"GET", "/fanout", http.StatusNoContent},
		{"GET", "/missing", http.StatusNotFound},
	} {
		t.Run(tc.method+tc.path, func(t *testing.T) {
			rec := httptest.NewRecorder()
			routes().ServeHTTP(rec, httptest.NewRequest(tc.method, tc.path, nil))
			if rec.Code != tc.want {
				t.Fatalf("got %d, want %d", rec.Code, tc.want)
			}
			if tc.want == http.StatusMethodNotAllowed && !strings.Contains(rec.Header().Get("Allow"), "GET") {
				t.Fatal("missing Allow: GET")
			}
		})
	}
}

func TestHTTP2(t *testing.T) {
	ts := httptest.NewUnstartedServer(routes())
	ts.EnableHTTP2 = true
	ts.StartTLS()
	defer ts.Close()
	res, err := ts.Client().Get(ts.URL + "/health")
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	if res.ProtoMajor != 2 || res.StatusCode != http.StatusNoContent {
		t.Fatalf("protocol %s, status %s", res.Proto, res.Status)
	}
}

func TestChannelHandler(t *testing.T) {
	rec := httptest.NewRecorder()
	channelHandler(rec, httptest.NewRequest(http.MethodGet, "/channel", nil))
	if rec.Code != http.StatusOK || rec.Body.String() != "work complete\n" {
		t.Fatalf("status %d, body %q", rec.Code, rec.Body.String())
	}
	t.Log("worker sent a result; handler wrote the response")
}
