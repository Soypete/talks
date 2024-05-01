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
When choosing to write to and from memory, there are two major type of opeations buffered and non-buffered I/o operations, 

who can tell me the difference? 

When to Use buffered I/O
- Improved Performance:
   * Buffered I/O reduces the frequency of actual system calls, leading to improved performance, especially when dealing with small reads or writes.
   * By batching data transfers, buffered I/O reduces the overhead of context switching and system call overhead.
- Reduced Latency:
   * Since data is buffered in memory before being written to or read from the underlying device, buffered I/O can reduce latency, especially in network or disk operations.
- Optimized Throughput:
   * Buffering allows for optimizing the use of underlying resources, such as minimizing the number of disk accesses or network packets sent, thereby improving overall throughput.
- Convenient Error Handling:
   * Buffered I/O simplifies error handling by allowing operations to complete in a batch, making it easier to manage errors and retries.


When to use non-buffered I/O
- Increased Memory Usage:
   * Buffered I/O requires additional memory allocation for buffers, which can increase memory usage, especially if large buffers are used or if multiple buffered streams are active concurrently.
- Potential Data Loss:
   * Since data is buffered in memory before being flushed to the underlying device, there is a risk of data loss in case of program crashes or unexpected failures before the buffer is written out.
- Complexity in Synchronization:
   * Buffered I/O introduces complexities in synchronization, especially in concurrent environments, where proper synchronization mechanisms must be implemented to ensure data integrity and avoid race conditions.
- Delayed I/O:
   * Due to buffering, there can be a delay between when data is written to or read from the buffer and when it is actually processed by the underlying device, which may not be desirable in real-time or low-latency applications.

---

## **Database conentions:**
- Creates a connetion for interacting with data over a databse protocol

Certainly! In Go's `database/sql` package, which is used for working with SQL databases, the `io.Reader` and `io.Writer` interfaces are utilized for handling database queries and results. Here's a simplified example of how these interfaces are used:

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

1. We import the required packages (`database/sql`, `github.com/go-sql-driver/mysql`).
2. We open a connection to a MySQL database using `sql.Open`, which returns a `*sql.DB` representing the database connection.
3. We execute a query using `db.Query`, which returns a `*sql.Rows` representing the result set. We then use `rows.Next` to iterate through the rows and `rows.Scan` to read data into variables, utilizing the `io.Reader` interface.
4. We prepare an SQL statement using `db.Prepare`, which returns a `*sql.Stmt` representing the prepared statement.
5. We write data using `stmt.Exec`, which executes the prepared statement, utilizing the `io.Writer` interface to write data to the database.

This example demonstrates how Go's `database/sql` package leverages the `io.Reader` and `io.Writer` interfaces for reading query results and writing data to a database, respectively.
---

## **Network I/O (e.g., TCP/UDP)**: http.ReadResponse
- Creates a conenction to the data packets sent over an Internet protocol

Certainly! In a WebSocket call in Go, the `io.Reader` and `io.Writer` interfaces are commonly used to read incoming messages from the WebSocket connection and write outgoing messages to the WebSocket connection. Here's an example using the popular `gorilla/websocket` package:

First, make sure to install the `gorilla/websocket` package if you haven't already:

```bash
go get github.com/gorilla/websocket
```

Now, here's an example of how you can use the `io.Reader` and `io.Writer` interfaces in a WebSocket call:

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

In this example:

1. We import necessary packages, including `io`, `log`, `net/http`, and `github.com/gorilla/websocket`.
2. We define an `echoHandler` function that upgrades HTTP connections to WebSocket connections using `websocket.Upgrader` and then listens for incoming messages.
3. Inside the `for` loop, we use `conn.ReadMessage()` to read messages from the WebSocket connection, which returns an `io.Reader` interface for reading the message.
4. We process the received message (in this case, just echo it back) and then use `conn.WriteMessage()` to write a response message back to the WebSocket connection, utilizing the `io.Writer` interface for writing.

This example demonstrates a simple WebSocket echo server in Go, showcasing the usage of `io.Reader` and `io.Writer` interfaces for handling incoming and outgoing messages in a WebSocket call.

---
   
## **Network I/O (e.g., TCP/UDP)**: http.Write

---

## Demo

[video]()
[code](https://github.com/Soypete/read_write_benchmark)

---

## In Summary
- Know your code.

---

## Contact

- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---
## REFERENCE:
* 