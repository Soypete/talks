---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('../images/weave_theme.png')
footer: '[Example Code](https://github.com/Soypete/Golang-Generics-Example)'
marp: true
---

# Generics in Go: Summary, Features and Cautions from go 1.18
Miriah Peterson

___

## Bio
- [DRE](https://medium.com/weave-lab/introduction-to-data-reliability-engineering-2ddacf7122b7) @ Weave
- Software development streamer [@soypete01](https://www.twitch.tv/soypete01)
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)

![bg right](../images/Gamer_2.png)

---

## Learn More About Go

- [Production Go: Patterns and Anti-patterns for Memory Mamangement](https://www.oreilly.com/live-events/production-go-patterns-and-anti-patterns/0636920072265/0636920072264/)
- [GoWest Conference](https://gowestconf.com)

![bg right](../images/oriely.png)

---
## Weave is HIRING

- [SRE](https://grnh.se/87a333853us)
- [SWE 4](https://grnh.se/90fb5fb03us)
- [Backend Engineer](https://grnh.se/249a85c43us)

![bg right](../images/weave.png) <!--- weave building picture--->

---

## What are Generics? 
<!--- 
parametric programming
--->
_**Parametric Polymorphism** is a way to make a language more expressive, while still maintaining full static type-safety._ ([wikipedia](https://en.wikipedia.org/wiki/Parametric_polymorphism))

In many programming languages (C++/Rust) the heavily lifting of type-safety generics is done by the compiler.  

---
## Generics in Go
_The generic dilemma is this: do you want slow programmers, slow compilers and bloated binaries, or slow execution times?_ (-Russ Cox, [The Generic Dilema](https://research.swtch.com/generic))

---
## Generics in Go
_The generic dilemma is this: do you want slow programmers, slow compilers and bloated binaries, or slow execution times?_ (-Russ Cox, [The Generic Dilema](https://research.swtch.com/generic))

1. Syntax and how to use generics
---
## Generics in Go
_The generic dilemma is this: do you want slow programmers, slow compilers and bloated binaries, or slow execution times?_ (-Russ Cox, [The Generic Dilema](https://research.swtch.com/generic))

1. Syntax and how to use generics
2. Compile time and binary size
---
## Generics in Go
_The generic dilemma is this: do you want slow programmers, slow compilers and bloated binaries, or slow execution times?_ (-Russ Cox, [The Generic Dilema](https://research.swtch.com/generic))

1. Syntax and how to use generics
2. Compile time and binary size
3. Execution time with benchmarks
---

## Using Generics

```go
func SumInts(m map[string]int64) int64 {
    var s int64
    for _, v := range m {
        s += v
    }
    return s
}

func SumFloats(m map[string]float64) float64 {
    var s float64
    for _, v := range m {
        s += v
    }
    return s
}
```
[tutorial](https://go.dev/doc/tutorial/generics)

---
## Using Generics
<!---
key parts of the syntax
* function declaration
* contraints
* parameters
--->
```go
// SumIntsOrFloats sums the values of map m. It supports both int64 and float64
// as types for map values.
func SumIntsOrFloats[K comparable, V int64 | float64](m map[K]V) V {
    var s V
    for _, v := range m {
        s += v
    }
    return s
}
```
[tutorial](https://go.dev/doc/tutorial/generics)

---

## Using Types
<!--- verbally credit bill kenedy for the example
GO to code here and run the last command on various type --->
```go
type vector[T any] []T

func (v vector[T]) last() (T, error) {
    var zero T
    if len(v) == 0 {
        return zero, fmt.Errorf("empty vector")
    }
    return v[len(v)-1], nil
}
```
---
## Using Types
<!--- verbally credit bill kenedy for the example --->
```go
// Zero value construct
var vGenInt vector[int]
var vGenStr vector[string]

// Non-zero value construct
vGenInt = vector{1, 2, 3}
vGenStr = vector{"a", "b", "c"}
```
---
## Using Structs
Declaring your own type with a struct
<!--- this is an example for a linked list
I would use the example from mastering go if I have time to add
--->

```go
type node[T any]struct{
    Data T
    next *node[T]
    prev *node[T]
}

```
---
## Using Behavior
This isn't new to Go! it is just a slightly different way to write interfaces

---
## Using Behavior
```go
type user struct{
    name string 
}
func (u Use) String() string {
    return u.name
}
type Stringer interface{
    String() string
}
type Concrete(u User){
    u.String()
}
type Polymoprhic(s Stringer){
    s.String()
}
```

---
## Best Practices
### Syntax

- Single Capital letters or Snake Case   for Type identifiers
    - K, V, Key, Value
- lower case letters for contraints
    - any, comparable, int64, float64
<!---
add the realease note here
from the vitess article
--->
---
## Execution time

```go
func BenchmarkSumGenInt(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SumIntsOrFloats(BenchInts)
	}
func BenchmarkSumIntLarge(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SumInts(BenchInts)
	}
}
```
---

## Execution time

```go
func BenchmarkSumGenFloat(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SumIntsOrFloats(Benchfloats)
	}
}
func BenchmarkSumFloatLarge(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SumFloats(Benchfloats)
	}
}
```
---
## Execution time
<!--- run the example if you have time--->
![bg 80% ](../images/generics_nops.png)

---

## Best Practices
<!--- Use cases from the Vitess article--->
- Where you want to use same logic for different types of data
- Where you can parametrize functional helpers by their callback types. In some cases, it may allow the Go compiler to flatten them.
- When you have a good grasp on Memory Management and how to optimize it
([Planetscale blog](https://planetscale.com/blog/generics-can-make-your-go-code-slower))

*DO NOT USE UNTIL IT IS THE ONLY OPTION LEFT*

---

## Cautions

From [Planetscale blog](https://planetscale.com/blog/generics-can-make-your-go-code-slower)
* DO try to de-duplicate identical methods that take a string and a []byte using a ByteSeq constraint
* DO NOT attempt to use Generics to de-virtualize or inline method calls.<!---If you have already optimized for performance refactroing to generics will cause you to start all over --->
* DO NOT pass an interface to a generic function, under any circumstances. <!---functional programming with ggenerics is unsafe --->
* DO NOT rewrite interface-based APIs to use Generics.

---

## Cautions
from the [relsease notes](https://tip.golang.org/doc/go1.18)
* The Go compiler does not accept arguments of type parameter type with the predeclared functions real, imag, and complex
* The Go compiler does not support accessing a struct field x.f where x is of type parameter type even if all types in the type parameter's type set have a field f. <!---print example from the list--->
* Embedding a type parameter, or a pointer to a type parameter, as an unnamed field in a struct type is not permitted

---
## Questions
Thanks you for coming out to this talk!
[twitch.tv/soypete01](https://twitch.tv/soypete01)
[twitter.com/captainnobody1](https://twitter.com/captainnobody1)
[youtube.com/captainnobody1](https://www.youtube.com/channel/UCeXy81WS-kX9JBc2kNzrV3A)

---
## Resources
- [Generics slow down your code](https://planetscale.com/blog/generics-can-make-your-go-code-slower)
- [Generics and Value Types in Go](https://www.dolthub.com/blog/2022-04-01-fast-generics/)
- [Generics in Go](https://go.dev/blog/intro-generics)
- [Generic Dilema](https://research.swtch.com/generic)
- [Ultimate Go Notebook](https://courses.ardanlabs.com/courses/ultimate-go-notebook)
- [Learning Go](https://www.oreilly.com/library/view/learning-go/9781492077206/)
- [Mastering Go](https://www.packtpub.com/product/mastering-go-third-edition/9781801079310)

--- 
## Compile time and binary size
<!---how do we measure this--->

---
## GCShapes 
[proposal GCShape stenciling](https://github.com/golang/proposal/blob/master/design/generics-implementation-gcshape.md)
<!--- they say don't do recursion cause generics don't support them --->

---
## Dictionaries
[Design Spec](https://github.com/golang/proposal/blob/master/design/generics-implementation-dictionaries-go1.18.md)

<!--- dictionaries are not new to go they are actually how we presently store strings
leverages existing map paradigms to add contracts to types --->

---
## [Constraints](https://pkg.go.dev/golang.org/x/exp/constraints)
- type Complex
- type Float
- type Integer
- type Ordered
- type Signed
- type Unsigned