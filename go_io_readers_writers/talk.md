---
theme: default
paginate: true
marp: true
backgroundImage: url('../images/Template.png')
---

# Go's Byte Bridge: io.Reader and io.Writer deep dive
Miriah Peterson

---
## Never have I ever?
* Written a handleFunc() for an http.Server{}?
* Created an http.Request{} for an http.Client{}
* Read from a sq.DB?
* Writen to or read from a file?
* Accessed an env variable?
* Accepted a CLI flag or arguement?
<!--- every single one of these operations uses eithre the REader or the Writer interface--->

---

## What is I/O?

>In computing, input/output (I/O, i/o, or informally io or IO) is the communication between an information processing system, such as a computer, and the outside world, such as another computer system, peripherals, or a human operator
(https://en.wikipedia.org/wiki/Input/output)

---

## What is I/O?
In the go ecosystem we are mostly talking about from inside the go app's memory to outside the go apps memory.

<!--- In the cases where we run a Copy from one internal memory location ot another memory location (not common) the original location is marked by the garbage collection--->
---
## Readers

What is a reader?
```
type Reader interface {
	Read(p []byte) (n int, err error)
}
```
<!-- 

* where does is write
* how does it write
* when does it block the garbage collector
* how do channels play in --->

---
## Readers
> The io package specifies the io.Reader interface, which represents the read end of a stream of data.
(https://go.dev/tour/methods/21)

---
## Readers
It takes the data from one location and ingests it to another location inside the go app

<!---Find the expection and hold it in notes as an example. What are the copy operations that take bytes from one location in memory and move it to another? --->

---

## Writers

What is a writer?

```
type WriterAt interface {
	WriteAt(p []byte, off int64) (n int, err error)
}
```

It takes data from inside the fo app and sends it to another location outsite the go app.
<!--- I think io.Copy can be used internally. --->

---

## Inhereting Readers/Writers
```
// ReadWriter is the interface that groups the basic Read and Write methods.
type ReadWriter interface {
	Reader
	Writer
}

// ReadCloser is the interface that groups the basic Read and Close methods.
type ReadCloser interface {
	Reader
	Closer
}
```
[src/io/io.go](https://cs.opensource.google/go/go/+/master:src/io/io.go;l=131?q=ReadWriter&ss=go/go)

<!-- Here we need examples of some of the direct implemendations like ReadWriter -->

---
## How do I implement Readers and Writers? 
How many times are the io.Reader and io.Writer interfaces inmplemented inside the standard lib?
* Std lib [Reader](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
* Std lib [Writer](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
<!---138 implementations of just the reader interface in the std lib https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo and  161 of the writer interface https://cs.opensource.google/search?q=Write%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&sq=&ss=go%2Fgo as of 4/29/2024--->

---
##  I/O Patterns
When choosing to write to and from memory, there are two major type of opeations buffered and non-buffered I/o operations

---
##  I/O Patterns

Who can tell me the difference?

<!--- Add file write from example cod--->
---
##  File I/O
```go 
func readAllFile() {
	f, err := os.Open("twitchChat.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	_, err = io.ReadAll(f)
	if err != nil {
		log.Fatal(err)
	}
}
```
<!--- Add file write from example cod--->
---

## File I/O

When to use classic I/O patterns
* Does memory matter?
   <!---> Buffered I/O requires additional memory allocation for buffers, which can increase memory usage, especially if large buffers are used or if multiple buffered streams are active concurrently.
* High Synchronization
   <!--- Buffered I/O introduces complexities in synchronization, especially in concurrent environments, where proper synchronization mechanisms must be implemented to ensure data integrity and avoid race conditions.
* Realtime events
   <!---> Due to buffering, there can be a delay between when data is written to or read from the buffer and when it is actually processed by the underlying device, which may not be desirable in real-time or low-latency applications.

---

## Buffered I/O
Buffered I/O in Go is any read write operation in the [bufio moldule](https://pkg.go.dev/bufio). These operators store the data in memory before it sends the data outside the api.

---

## Buffered I/O
When to Use buffered I/O

* Optimized Throughput
   <!-- * Buffering allows for optimizing the use of underlying resources, such as minimizing the number of disk accesses or network packets sent, thereby improving overall throughput. -->
* Convenient Error Handling
   <!-- * Buffered I/O simplifies error handling by allowing operations to complete in a batch, making it easier to manage errors and retries. -->

---
## Buffered I/O (generated example)
``` go
func readFileBuf() {
	file, err := os.Open("twitchChat.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}
```
---

## Database I/O
Database drivers inmplent the io.Readers/Writers to manage the data stream between the data store and the go software app.

---

## Database I/O
```go
func readfromdb() {
	filename := "twitchchat.db"
	db, err := sql.open("sqlite3", filename)
	if err != nil {
		log.fatal(err)
	}
	defer db.close()

	rows, err := db.query("select * from chat")
	if err != nil {
		log.fatal(err)
	}
	for rows.next() {
		var id int
		var message string
		rows.scan(&id, &message)
	}
}
```

<!--- >
1. we import the required packages (`database/sql`, `github.com/go-sql-driver/mysql`).
2. we open a connection to a mysql database using `sql.open`, which returns a `*sql.db` representing the database connection.
3. we execute a query using `db.query`, which returns a `*sql.rows` representing the result set. we then use `rows.next` to iterate through the rows and `rows.scan` to read data into variables, utilizing the `io.reader` interface.
4. we prepare an sql statement using `db.prepare`, which returns a `*sql.stmt` representing the prepared statement.
5. we write data using `stmt.exec`, which executes the prepared statement, utilizing the `io.writer` interface to write data to the database.

where is the interaface actually implemented it is in the driver haha. https://github.com/lib/pq/blob/master/copy.go
--->
---

## I/O over the internet
In go, when we are making calls over ip, we are still using the io.reader/writer. all data is sent as a stream, so the chucks of bytes instead of being directly written are just sent as data in a packet.

---

## Network I/O

```go
func messageHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")

	_, err := fmt.Fprintf(w, testString)
	if err != nil {
		log.Println("Error writing message:", err)
	}
}
```
---

## Demo

[code](https://github.com/Soypete/read_write_benchmark)

---

## In Summary
* Every Go App leverages I/O operations
* There are lots of options for implementations of io.Reader and io.Writer
* What kinds of operations Readers and Writers have
* How to evaluate our Readers and Writers

---

## Contact

* [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
* [GitHub soypete](https://www.github.com/soypete)
* [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)
* [twitch](https://twitch.tv/soypetetech)

![bg right w:620](../images/sp_max_loulou.jpeg)
