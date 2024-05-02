---
theme: gaia
_class: lead
paginate: true
backgroundColor: #d9ffff
marp: true
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
* It takes the data from one location and ingests it to another location inside the go app

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

## Implementing Readers/Writers

<!-- Here we need examples of some of the direct implemendations like ReadWriter -->

---
## The interface in the Standard Lib
How many times are the io.Reader and io.Writer interfaces inmplemented inside the standard lib?
* Std lib [Reader](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
* Std lib [Writer](https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo)
<!---138 implementations of just the reader interface in the std lib https://cs.opensource.google/search?q=Read%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&ss=go%2Fgo and  161 of the writer interface https://cs.opensource.google/search?q=Write%5C(%5Cw%2B%5Cs%5C%5B%5C%5Dbyte%5C)&sq=&ss=go%2Fgo as of 4/29/2024--->

---
##  I/O Patterns
When choosing to write to and from memory, there are two major type of opeations buffered and non-buffered I/o operations

Who can tell me the difference?

<!--- Add file write from example cod--->
---
##  File I/O
* Created a connections for writing data over an os protocol

<!--- Add file write from example cod--->
---

## File I/O

When to use classic I/O patterns
* Does memory matter?
   <!---> Buffered I/O requires additional memory allocation for buffers, which can increase memory usage, especially if large buffers are used or if multiple buffered streams are active concurrently.
* High Synchronization:
   <!--- Buffered I/O introduces complexities in synchronization, especially in concurrent environments, where proper synchronization mechanisms must be implemented to ensure data integrity and avoid race conditions.
* Realtime events:
   <!---> Due to buffering, there can be a delay between when data is written to or read from the buffer and when it is actually processed by the underlying device, which may not be desirable in real-time or low-latency applications.

---

## Buffered I/O
Buffered I/O in Go is any read write operation in the [bufio moldule](). These operators store the data in memory before it sends the data outside the api.

---

## Buffered I/O
When to Use buffered I/O

* Optimized Throughput:
   <!-- * Buffering allows for optimizing the use of underlying resources, such as minimizing the number of disk accesses or network packets sent, thereby improving overall throughput. -->
* Convenient Error Handling:
   <!-- * Buffered I/O simplifies error handling by allowing operations to complete in a batch, making it easier to manage errors and retries. -->

---
## Buffered I/O

<!---TODO: add to the benchmarking examples --->
``` go
package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	// Open the text file for reading
	file, err := os.Open("example.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a new scanner for reading from the file
	scanner := bufio.NewScanner(file)

	// Iterate over each line in the file and print it
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}

	// Check for any errors during scanning
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

```
---

## Database conentions:
Database drivers inmplent the io.Readers/Writers to manage the data stream between the data store and the go software app.


---

## Database conentions:
```go
package main

import (
    "database/sql"
    "fmt"
    "log"
    _ "github.com/go-sql-driver/mysql" // Import MySQL driver
)

func main() {
    // Open a connection to the MySQL database
    db, err := sql.Open("mysql", "username:password@tcp(localhost:3306)/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Execute a query and retrieve results
    rows, err := db.Query("SELECT id, name FROM users")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    // Iterate through the rows and read data using io.Reader
    for rows.Next() {
        var id int
        var name string
        if err := rows.Scan(&id, &name); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("ID: %d, Name: %s\n", id, name)
    }
    if err := rows.Err(); err != nil {
        log.Fatal(err)
    }

<!---TODO: break here and make a new function using exec --->

    // Example of writing data using io.Writer
    stmt, err := db.Prepare("INSERT INTO users(id, name) VALUES (?, ?)")
    if err != nil {
        log.Fatal(err)
    }
    defer stmt.Close()

    // Write data using io.Writer interface
    _, err = stmt.Exec(1, "Alice")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Data inserted successfully.")
}
```

In this example:
<!--- >
1. We import the required packages (`database/sql`, `github.com/go-sql-driver/mysql`).
2. We open a connection to a MySQL database using `sql.Open`, which returns a `*sql.DB` representing the database connection.
3. We execute a query using `db.Query`, which returns a `*sql.Rows` representing the result set. We then use `rows.Next` to iterate through the rows and `rows.Scan` to read data into variables, utilizing the `io.Reader` interface.
4. We prepare an SQL statement using `db.Prepare`, which returns a `*sql.Stmt` representing the prepared statement.
5. We write data using `stmt.Exec`, which executes the prepared statement, utilizing the `io.Writer` interface to write data to the database.

where is the interaface actually implemented it is in the driver haha. https://github.com/lib/pq/blob/master/copy.go
--->
---

## I/O over the Internet:
In go, when we are making calls over IP, we are still using the io.Reader/Writer. All data is sent as a stream, so the chucks of bytes instead of being directly written are just sent as data in a packet.

---

## Network I/O (Websocket):

```go
package main

import (
	"io"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}
	defer conn.Close()

	for {
		// Read message from the WebSocket connection
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			if err != io.EOF {
				log.Println("Error reading message:", err)
			}
			break
		}

		// Process the received message (for demonstration, just echo it back)
		log.Printf("Received message: %s\n", message)

		// Write response back to the WebSocket connection
		err = conn.WriteMessage(messageType, message)
		if err != nil {
			log.Println("Error writing message:", err)
			break
		}
	}
}

func main() {
	http.HandleFunc("/echo", echoHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```
<!---
In this example:

1. We import necessary packages, including `io`, `log`, `net/http`, and `github.com/gorilla/websocket`.
2. We define an `echoHandler` function that upgrades HTTP connections to WebSocket connections using `websocket.Upgrader` and then listens for incoming messages.
3. Inside the `for` loop, we use `conn.ReadMessage()` to read messages from the WebSocket connection, which returns an `io.Reader` interface for reading the message.
4. We process the received message (in this case, just echo it back) and then use `conn.WriteMessage()` to write a response message back to the WebSocket connection, utilizing the `io.Writer` interface for writing.

This example demonstrates a simple WebSocket echo server in Go, showcasing the usage of `io.Reader` and `io.Writer` interfaces for handling incoming and outgoing messages in a WebSocket call.
--->

<!-- ---
   
## Network I/O (e.g., TCP/UDP): http.Write -->

---

## Demo

[video]()
[code](https://github.com/Soypete/read_write_benchmark)

---

## In Summary
Know your code.

---

## Contact

* [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
* [GitHub soypete](https://www.github.com/soypete)
* [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---
## REFERENCE:
* 