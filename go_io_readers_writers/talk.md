---
theme: gaia
_class: lead
paginate: true
backgroundColor: #d9ffff
marp: true
---

# Exploring Go's io.Reader and io.Writer Interfaces
Miriah Peterson

---
## Never have I ever?
- Written a handleFunc() for an http.Server{}?
- Created an http.Request{} for an http.Client{}
- Read from a sq.DB?
- Writen to or read from a file?
- Accessed an env variable?
- Accepted a CLI flag or arguement?
<!--- every single one of these operations uses eithre the REader or the Writer interface--->

---
# Go's most powerful interfaces: io.Reader + io.Writer
* Std lib [Reader](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
* Std lib [Writer](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
<!---138 implementations of just the reader interface in the std lib https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo and  161 of the writer interface https://cs.opensource.google/search?q=Write%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&sq=&ss=go%2Fgo as of 4/29/2024--->

---
## Readers
<!-- deep dive into into I/O writer for http, memory, db, channels, etc

- where does is write
- how does it write
- when does it block the garbage collector
- how do channels play in --->

> The io package specifies the io.Reader interface, which represents the read end of a stream of data.

https://go.dev/tour/methods/21

---

##  **File I/O**: os.File
- Creates a connections for reading data over an os protocol

---
##  **File I/O**: os.Create
- Created a connections for writing data over an os protocol

---


## **Buffered I/O**
   - Advantages of buffering
   - When to use buffered I/O
   - Demo: comparing buffered vs. unbuffered performance

---

## **Database conentions:**
   - Using io.Pipe for inter-process communication
   - Concurrency patterns with io.Reader and io.Writer
   - Pitfalls in concurrent I/O operations

---

## **Network I/O (e.g., TCP/UDP)**: http.ReadResponse
- Creates a conenction to the data packets sent over an Internet protocol
---
   
## **Network I/O (e.g., TCP/UDP)**: http.Write
   - Performance considerations
   - Best practices for handling network I/O
   - Security considerations

---

## Demo
<!--- benchmark of several functions with memory on/ maybe pprof --->

---

## In Summary
.

---

## Contact

- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---
## REFERENCE:
* 