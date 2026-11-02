//go:build go1.27

package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"testing/synctest"
	"time"
)

func TestSlowEndpoint(t *testing.T) {
	synctest.Test(t, func(t *testing.T) {
		ts := httptest.NewTestServer(t, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			time.Sleep(5 * time.Second)
			w.WriteHeader(http.StatusNoContent)
		}))
		resp, err := ts.Client().Get(ts.URL)
		if err != nil {
			t.Fatal(err)
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusNoContent {
			t.Fatal(resp.Status)
		}
	})
}
