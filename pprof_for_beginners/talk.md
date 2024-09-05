---
theme: gaia
_class: lead
paginate: true
color: white
backgroundImage: url('../images/p99_template.png')
marp: true
---

# pprof for Beginners

Miriah Peterson

---

## Intro

<!--- I am a pprof beginner like many of you. When I started I literally had to ask twitch chat how to run it because I couldn't file reliable docs via google search. Now, I know exactly what I demo'd today. Nothing more. --->

* Programs use memory and cpu resources
* Microservices/cloud deployments have conditioned developers ignore how software interacts with its environment
* Understanding how your program uses its memory and cpu can help developers understand some weak points of their services.

---

## Service Weak Points

* What is a memory leak?
* What is a database collision?
* What is a mutex loc?
* What is the job of the garbage collector?
* Should I share memory across my goroutines?
* Should this procedure be inlined?
* How is the compiler optimizing my code?

---

## What is Profiling

> In software engineering, profiling ("program profiling", "software profiling") is a form of dynamic program analysis that measures, for example, the space (memory) or time complexity of a program, the usage of particular instructions, or the frequency and duration of function calls.

 [Wikipedia - Profiling(computer programming)](<https://en.wikipedia.org/wiki/Profiling_(computer_programming)#:~:text=In%20software%20engineering%2C%20profiling%20(%22,and%20duration%20of%20function%20calls.)>)
 
---

## What is pprof

<!-- After this slide we are going to go into some of the usecases that I have found very helpful  -->

> pprof is a tool for visualization and analysis

* it leverages protobuf files to capture data about performance
* these protobuf files can be read and analyzed via web ui or command line
* it is shipped with the go std library

---

# What information can pprof provide?

---

## What does pprof do - allocations

> _allocs_: A sampling of all past memory allocations

---

## What does pprof do - memory

> _heap_: A sampling of memory allocations of live objects. You can specify the gc GET parameter to run GC before taking the heap sample.

---

## What does pprof do - cpu

> _profile_: CPU profile. You can specify the duration in the seconds GET parameter. After you get the profile file, use the go tool pprof command to investigate the profile.

---

## What does pprof do - goroutine

> _goroutine_: Stack traces of all current goroutines. Use debug=2 as a query parameter to export in the same format as an unrecovered panic.

---

## What does pprof do - others

<!---If you forget these they are provided on the pprof default web page --->

* _block_: Stack traces that led to blocking on synchronization primitives
* _cmdline_: The command line invocation of the current program
* _mutex_: Stack traces of holders of contended mutexes
* _threadcreate_: Stack traces that led to the creation of new OS threads
* _trace_: A trace of execution of the current program. You can specify the duration in the seconds GET parameter. After you get the trace file, use the go tool trace command to investigate the trace.

---

## Setup pprof - server

```
import (
	_ "net/http/pprof"
)
func main() {
	// run pprof
	go func() {
		fmt.Println(http.ListenAndServe("localhost:6060", nil))
	}()
    ...
}
```

---

## Setup pprof - files

```
if err := pprof.StartCPUProfile(f); err != nil {
	log.Fatal("could not start CPU profile: ", err)
}

// remove unused heap allocations

runtime.GC()
if err := pprof.WriteHeapProfile(f); err != nil {
	log.Fatal("could not write memory profile: ", err)
}
```

---

## Setup pprof - chi router

```
import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func main() {
	r := chi.NewRouter()
	r.Mount("/debug", middleware.Profiler())
}
```

[chi](https://go-chi.io/#/pages/middleware?id=profiler)

---

## Using pprof - default

After adding pprof driver to your go server, default web page is available via server for consuming these endpoints.

* code for this example is available [here](https://github.com/Soypete/Production-Go-Examples)
* [demo](https://youtu.be/vSdOAzrVvaU)

---

## Using pprof - cli

To access and analyze pprof data, you can use the cli command:

```
go tool pprof http://localhost:6060/debug/pprof/allocs
```

[demo](https://youtu.be/Fuz3fNg30cU)
[additional docs](https://github.com/google/pprof/tree/main/doc)

---

## Using pprof - UI

<!--- demo --->

You can also access and analyze pprof data via a helpful web UI.
_If you want to access the interactive web UI you will need to install the [graphviz tool](https://graphviz.org/download/)_

```
go tool pprof -http=:18081 http://localhost:6060/debug/pprof/profile\?seconds\=30
```

[demo](https://www.youtube.com/watch?v=v6skRrlXsjY)

---

## Using pprof - save files

If you have cached your data, access it directly from the stored protobuf files

```
go tool pprof ex-4-benchmarking/solution/cpu.prof
```

---

## pprof FAQ

* Should I run pprof in production?
* Does it impact my go application?
* How do I learn more about prof?

---

## In Summary

Use pprof as a tool for debugging and improving your code. It will unlock the memory contingent tools like mutexes, goroutines, cpu threading, and go channels.

---

## Contact

* [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
* [GitHub soypete](https://www.github.com/soypete)
* [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---

## REFERENCE:

* https://github.com/google/pprof
* https://perf.wiki.kernel.org/index.php/Main_Page
* https://github.com/google/pprof/blob/main/doc/README.md
* https://en.wikipedia.org/wiki/Profiling_(computer_programming)#:~:text=In%20software%20engineering%2C%20profiling%20(%22,and%20duration%20of%20function%20calls)
* https://go.dev/doc/diagnostics#profiling
* https://www.infoq.com/articles/debugging-go-programs-pprof-trace/

---

* https://pkg.go.dev/runtime/pprof
* https://pkg.go.dev/net/http/pprof
* https://go.dev/blog/pprof
* https://en.wikipedia.org/wiki/Call_stack#:~:text=In%20computer%20science%2C%20a%20call,to%20just%20%22the%20stack%22.
* https://en.wikipedia.org/wiki/Point_location
* https://go-chi.io/#/pages/middleware?id=profiler
