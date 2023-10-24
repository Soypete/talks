---
theme: gaia
_class: lead
paginate: true
backgroundColor: #d9ffff
marp: true
---

# Go Install PARTY!

Miriah Peterson

---

## What we will do
<!---I know there are plenty of Gophers here. (in this concurrency) --->
* Install Go
* Create project with project templates
* Setup testing and linting
* Push to github with Github actions

---

## Install

Use [webi](https://webinstall.dev/) to quickly install 
```
$ curl -sS https://webi.sh/golang | sh
```

---

## Check

```
$ go version
```

---

## Create a project

```
$ go install golang.org/x/tools/cmd/gonew@latest
```

---

## Create a project

```
$ gonew soypete/go-template-repo soypete/demoservice
```

---

## Setup testing

```
$ go get -u github.com/rakyll/gotest
```

---

## Setup testing

```
$ gotest ./...
```

---
## Setup Linting

```
$ curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.55.0

$ golangci-lint --version
```

---

## Setup testing

```
$ golangci-lint run
```

---

## Setup CI Check
In you repo create the following file `.github/workflows/go.yml`

Add the following to that file

```
name: Go

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:

  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v3
      with:
        go-version: 1.18

    - name: Build
      run: go build -v ./...


```
---

## Sponsor or contact

[Github Sponsor]()
[Course]()
[Twitch]()
