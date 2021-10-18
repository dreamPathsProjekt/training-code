# Go Introductory Guide - Best Practices

- [Go Introductory Guide - Best Practices](#go-introductory-guide---best-practices)
  - [Resources](#resources)
  - [VsCode settings for GVM](#vscode-settings-for-gvm)
  - [Udemy Courses](#udemy-courses)
    - [Go Complete](#go-complete)
      - [Go main commands](#go-main-commands)
      - [Packages Executable vs Reusable](#packages-executable-vs-reusable)
      - [Deeper: Variables/Functions/Slices/Types](#deeper-variablesfunctionsslicestypes)
      - [Structs & Pointers](#structs--pointers)
      - [Maps](#maps)
      - [Interfaces](#interfaces)
      - [Channels & Go Routines](#channels--go-routines)
    - [GRPC MAsterclass](#grpc-masterclass)
    - [Concurrency in GO](#concurrency-in-go)
    - [Go Serverless](#go-serverless)
    - [Go Design Patterns](#go-design-patterns)
      - [SOLID Principles](#solid-principles)
      - [Builder Pattern](#builder-pattern)
      - [Factory Pattern](#factory-pattern)
      - [Prototype](#prototype)
      - [Singleton](#singleton)
    - [Go Rest Microservices](#go-rest-microservices)
  - [Configuration & VSCode issues](#configuration--vscode-issues)
  - [Interesting SO Questions](#interesting-so-questions)
  - [Notes from `koslib`](#notes-from-koslib)

## Resources

- [https://github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout)
- [https://golang.org/doc/faq](https://golang.org/doc/faq)
- [https://golang.org/doc/effective_go](https://golang.org/doc/effective_go)
- Google Wire for DI on complicated projects
  - [https://github.com/google/wire/blob/main/_tutorial/README.md](https://github.com/google/wire/blob/main/_tutorial/README.md)
  - [https://go.dev/blog/wire](https://go.dev/blog/wire)
- [https://betterprogramming.pub/7-code-patterns-in-go-i-cant-live-without-f46f72f58c4b](https://betterprogramming.pub/7-code-patterns-in-go-i-cant-live-without-f46f72f58c4b)
- [https://talks.golang.org/2012/10things.slide#1](https://talks.golang.org/2012/10things.slide#1)
- [https://yourbasic.org/golang/iota/](https://yourbasic.org/golang/iota/)

Testing/Mocking pkgs

- [Mockery](https://github.com/vektra/mockery)
  - [https://medium.com/@thegalang/testing-in-go-mocking-mvc-using-testify-and-mockery-c25344a88691](https://medium.com/@thegalang/testing-in-go-mocking-mvc-using-testify-and-mockery-c25344a88691)
- [Filesystem Mock](https://pkg.go.dev/testing/fstest)
- [Abstract FS](https://github.com/spf13/afero)

## VsCode settings for GVM

- Better isolation: project settings in `<project>/.vscode/settings.json`

```JSON
{
    "go.gopath": "/home/dreampaths/.gvm/pkgsets/go1.16.8/global",
    "go.goroot": "/home/dreampaths/.gvm/gos/go1.16.8",
}
```

## Udemy Courses

### Go Complete

- [https://www.udemy.com/course/go-the-complete-developers-guide](https://www.udemy.com/course/go-the-complete-developers-guide)
- [Diagrams](https://github.com/StephenGrider/GoCasts/tree/master/diagrams)

#### Go main commands

- `run` - compile and run one or two files
- `build` - compile packages
- `fmt` - formats all source code in current dir
- `install` - compile and install package
- `get` - download module or package source code
- `test` - runs tests

#### Packages Executable vs Reusable

- The name `main` of the package determines if executable `package main` -> `go build` -> `main/main.exe`
- `package main` must contain `main` function
- To have multiple executable packages in same project `<module>/cmd/helloworld1/main.go`, `<module>/cmd/helloworld2/main.go`. All packages under `cmd` folder are using declaration `package main` and are executable (produce binary outputs)
- Naming conventions
  - `cmd` contains executable packages
  - `pkg` contains publicly exposed & reusable code (functions, structs)
  - `internal` contains privately used code [https://dave.cheney.net/2019/10/06/use-internal-packages-to-reduce-your-public-api-surface](https://dave.cheney.net/2019/10/06/use-internal-packages-to-reduce-your-public-api-surface)
  - `internal/` is a special directory name recognised by the go tool which will prevent one package from being imported by another unless both share a common ancestor.
  - You can only declare a method with a __receiver whose type is defined in the same package as the method__. You cannot declare a method with a receiver whose type is defined in another package (which includes the built-in types such as int, func etc.). This is the reason why built-in types (primitives etc.) have to be __wrapped in a custom type__, to write receiver methods.
    - The reason is that if you could define methods on other packages' types, you could modify the behavior of other packages. This is because the method set of a given type can have an effect on how values of that type are used.
- [https://medium.com/rungo/everything-you-need-to-know-about-packages-in-go-b8bac62b74cc](https://medium.com/rungo/everything-you-need-to-know-about-packages-in-go-b8bac62b74cc)
- [https://medium.com/rungo/anatomy-of-modules-in-go-c8274d215c16](https://medium.com/rungo/anatomy-of-modules-in-go-c8274d215c16)

#### Deeper: Variables/Functions/Slices/Types

- Variables can be __initialized__ outside of a function, but cannot be __assigned__ a value. __No globals__ permitted.
- `append()` function for slices does not append new elements to existing slice, but returns a new slice (we usually assign the new slice to the same variable)

```Go
cards := []string{}

// Append takes initial cards slice as input, appends element and returns new slice, that we assign on cards variable.
cards = append(cards, "Six of Spades")
```

- Go documentation on `append()`

```Go
// The append built-in function appends elements to the end of a slice. If it has sufficient capacity, the destination is resliced to accommodate the new elements. If it does not, a new underlying array will be allocated. Append returns the updated slice. It is therefore necessary to store the result of append, often in the variable holding the slice itself:

slice = append(slice, elem1, elem2)
slice = append(slice, anotherSlice...)
// As a special case, it is legal to append a string to a byte slice, like this:

slice = append([]byte("hello "), "world"...)
```

- Subset (range) of slice (similar to Python) returns new slices

```Go
var fruits []string

// Select subset from and including index 0 up to and not including index 2
// Selects items fruits[0], fruits[1]
fruits[0:2]

// Select from start of the slice up to and not including index 2
fruits[:2]
// Select from index and include 2 up to and including the end of the slice.
fruits[2:]
```

- Multiple return values from function

```Go
// You can have arbitratrily multiple return values from a single function
func deal(d deck, handSize int) (deck, deck) {
  return d[:handSize], d[handSize:]
}
```

- __Naming convention__ Receiver instances to be 1 or at-most 2 letter names
- __Type conversion__

```Go
// Syntax type(value)

// Example string to byteslice (all characters into slice of bytes)
greeting := "Hello world"
[]byte(greeting)
```

- I/O Write file __permissions__ parameter, is only used when the file __doesn't exist__

```Go
import "io/ioutil"

// If file out.txt doesn't exist, create a new file with Linux permissions 0666 - Anyone can read and write (no execute)
filename := "out.txt"
err := ioutil.WriteFile(filename, []byte("Helloworld"), 0666)
```

- __Shuffle__ a slice - no std library package

```Go
// Algorithm: For each index, element in slice
// Generate a randomNumber between 0 and len(slice) - 1
// Swap current element with slice[randomNumber]

import (
  "math/rand"
  "time"
)

type deck []string

func (d deck) shuffle() {
  // Optional random number generation. Default Source type (interface) can be used, but randomization sequence happens in the same way, for subsequent runs.
  // Why: Default Source struct uses the same exact seed value (source of randomness). This is due to Source struct initialization.
  source := rand.NewSource(time.Now().UnixNano())
  // Creates new Rand type object.
  r := rand.New(source)

// We only care for the index not card.
  for i := range d {
    // Intn takes param as range of integers from 0 - a non-negative pseudo-random number in [0,n). It panics if n <= 0.
    newPosition := r.Intn(len(d) - 1)

    // This swap is valid in Go (similar to Python)
    d[i], d[newPosition] = d[newPosition], d[i]
  }
}
```

#### Structs & Pointers

- String formatted output of struct

```Go
var alex person

// %+v outputs all field names and values
fmt.Printf("%+v", alex)

// Structs can be updated as (alternative to literal notation)
alex.firstName = "Alex"
alex.lastName = "Anderson"
```

- Struct embedding & function receivers updates

```Go
type contactInfo struct {
  email   string
  zipCode int
}

// Compositional way - Can only use contact fields and methods (receiver functions) by using contact field.
type person struct {
  firstName string
  lastName  string
  contact   contactInfo
}

// Embedding (anonymous field) - Implicitly the field name is called contactInfo. Allows to raise embedded fields & methods (receiver functions).
type personEmbed struct {
  firstName string
  lastName  string
  contactInfo
}

// Instance cannot be updated since p is passed by value. The p VALUE (copy) is updated.
// It needs a pointer receiver of person to update the instance.
func (p person) updateName(name string) {
  p.firstName = name
}

func (p *person) updateNamePointer(name string) {
  // *p = give me access to the instance, the pointer points at
  // Parethenses are used to avoid doing pointer operation on field firstName (precedence)
  // Example *p.firstName does the pointer value operation on p.firstName variable
  // (*p).firstName does the pointer value operation on p and then accesses firstName.
  (*p).firstName = name
}

func main() {
  jim := person{}
  jim.firstName = "Jim"
  jim.updateName("Jimmy")
  println(jim.firstName)
  // output is still "Jim"

  // & gives the memory address of the variable
  // * gives the value a memory address (pointer) is pointing at
  // * on function signatures (receivers/arguments), it means pointer of type
  jimPointer := &jim
  jimPointer.updateNamePointer("Jimmy")
  println(jim.firstName)
  // output is "Jimmy"

  // Pointer shortcut - equivalent without variable holding pointer to jim
  // This works because a pointer receiver of a type can also accept the type itself.
  // Implicitly it is inferred that the address of the type should be used.
  jim.updateNamePointer()
  println(jim.firstName)
  // output is "Jimmy"
}
```

- Gotchas with pointers - Reference vs Value Types

In general Go is using __pass by value__ except for __reference types__ such as slice, since slice already has a pointer inside its structure. A slice pointer is copied as passed by value but __POINTS TO THE SAME  UNDERLYING ARRAY__.

This is based on the fact that slice is a __composite__ data structure, a record of `ptr to head`, `length` & `capacity` & an __underlying array__ that `ptr to head` points to.

__Reference__ types:

- slices
- maps
- channels
- pointers
- functions (can be passed as arguments to functions)

```Go
func main() {
  mySlice := []string{"Hi", "There"}

  updateSlice(mySlice)

  // Mutation works, no pass by value on slice
  fmt.Println(mySlice)
  // output [Bye There]

  // This is valid code and dereference will undo what the reference operator does
  fmt.Println(*&mySlice)
}

// Pass by value ? Yes, slice pointer is copied but PONTS TO THE SAME ARRAY.
func updateSlice(s []string) {
  s[0] = "Bye"
}
```

#### Maps

- Declarations

```Go
// Map of string keys with string values - literal
colors := map[string]string{
  "red": "#ff0000",
  "green": "#4bf745",
}

// Variable declaration - zero initialization (empty map)
var colors map[string]string

// make equivalent (but different, see below) - zero initialization (empty map)
colors := make(map[string]string)

// value assignment
colors["white"] = "#ffffff"
// delete key value pair
delete(colors, "white")
```

- `make` vs `new` (vs a variable declaration)
  - make and new are built-in functions golang uses to allocate memory and allocate memory on the heap. make allocates and initializes memory.New just clears memory and does not initialize it.
  - make returns the reference type itself; new returns a pointer to the type.
  - make can only be used to allocate and initialize data of slice, map, channel type; new can allocate any type of data.
  - [https://stackoverflow.com/questions/9320862/why-would-i-make-or-new](https://stackoverflow.com/questions/9320862/why-would-i-make-or-new)
  - [https://stackoverflow.com/questions/25543520/declare-slice-or-make-slice](https://stackoverflow.com/questions/25543520/declare-slice-or-make-slice)
  - Simple declaration `var s []int` __does not allocate memory and s points to nil__, while `s := make([]int, 0)` allocates memory and s points to memory to a slice with 0 elements. Usually, the first one is more idiomatic if you don't know the exact size of your use case.

- `map` vs `struct`
  - Struct keys don't support indexing (cannot iterate a struct), while map keys are __indexed__.
  - Map is a __reference type__, struct is a __value type.__
  - In struct you need to know all of the fields at compile time, map not needed (add and remove keys at runtime).
  - Maps are used to represent a __collection of related properties__, structs are a thing with lot of different properties.

#### Interfaces

- [https://betterprogramming.pub/a-comprehensive-guide-to-interfaces-in-go-6a945b795db](https://betterprogramming.pub/a-comprehensive-guide-to-interfaces-in-go-6a945b795db)

- Interfaces are an example of __subtyping polymorphism__ [https://en.wikipedia.org/wiki/Polymorphism_(computer_science)](https://en.wikipedia.org/wiki/Polymorphism_(computer_science))
  - __Ad-hoc polymorphism:__ function, method, operator overloading. No support from Go [https://golang.org/doc/faq#overloading](https://golang.org/doc/faq#overloading)
    - Can support __variadic arguments__ in functions, of same type.
  - __Parametric polymorphism:__ Generics (soon to be introduced in a future Go version)

- Interface are also an example of __structural typing__ where behaviour of a type (methods) dictates whether the type can implement an interface. This is also called __implicit implementation.__
  - __Nominal typing__ is an example where the implementation (equivalence) of an interface is based on __explicit static declaration__ of the sub-typing (e.g. by using `implements` keyword)
    - In computer science, a type system is a nominal or nominative type system (or name-based type system) if compatibility and equivalence of data types is determined by explicit declarations and/or the name of the types. Nominal systems are used to determine if types are equivalent, as well as if a type is a subtype of another. Nominal type systems contrast with structural systems, where comparisons are based on the structure of the types in question and do not require explicit declarations. [https://en.wikipedia.org/wiki/Nominal_type_system](https://en.wikipedia.org/wiki/Nominal_type_system)

- Interfaces cannot be used as __receivers__
- [Interfaces can also be implemented by non-struct types](https://golangbyexample.com/non-struct-type-implementing-interface-go/)
- When a function receiver is not used, we can ommit the instance (just declare the type)

```Go
type englishBot struct {}

func (englishBot) getGreeting() {
  // Receiver eb is not used, thus no need to be declared on receiver signature.
  // Similar to static method. Useful for interface implementation, otherwise an anti-pattern.
  return "Hi There!"
}
```

- Cannot have functions with __identical names__, unless they use __receivers__ of different type.
  - [https://medium.com/rungo/anatomy-of-methods-in-go-f552aaa8ac4a](https://medium.com/rungo/anatomy-of-methods-in-go-f552aaa8ac4a)

- Cannot __create a value of non-concrete type__ - interface
- To __implement__ an interface a type must implement all function signatures. Otherwise run-time error of `runtime error: invalid memory address or nil pointer dereference` is thrown.
- Implementing only __part__ of an interface and __delegating the rest to an embedded interface__ of the same type is perfectly valid. However the concrete type, has to have the embedded type not nil.
- Interfaces __are not generic types.__
- Interfaces are __contract types.__ Treat them as important in the design process.
- __Exported Interfaces__ from package can be implemented, from another package.

- Interface composition example in the std library

```Go
// package net/http
type Response struct {
  Status     string // e.g. "200 OK"
  StatusCode int    // e.g. 200
  Proto      string // e.g. "HTTP/1.0"
  ProtoMajor int    // e.g. 1
  ProtoMinor int    // e.g. 0

// ...

// Struct field as interface type
Body io.ReadCloser

// ...
}


// package io
// ReadCloser (type of http.Response.Body field) uses embedded interface types
// To satisfy a "composite" interface, we need to satisfy the requirements of both interfaces.
// It also means that a "composite" interface can be passed as argument types that require one of the embedded interfaces
// Example: use io.ReadCloser in arguments typed with io.Reader or io.Closer.
type ReadCloser interface {
  Reader
  Closer
}

type Reader interface {
  Read(p []byte) (n int, err error)
}

type Writer interface {
  Write(p []byte) (n int, err error)
}

type Closer interface {
  Close() error
}
```

- `io.Reader` interface uses input `[]byte` and __updates the input slice (usually empty) with data read__, and returns an integer, number of bytes read and `error`. Basically `.Read()` consumes an input from inside (a field) the caller struct and transforms it to `[]byte`
- `Read()` function (at least in `net/http.Response` implementation) does not __grow__ the slice in size if needed, but reads until slice is full.

```Go
resp, _ := http.Get("https://google.com")

// Allocate initialization space
bs := make([]byte, 99999)

// We do not care about number of bytes and ignore error.
resp.Body.Read(bs)

// bs []byte slice should be filled with incoming data from resp.Body
// Casting to string is used to avoid output of a list of byte integers
fmt.Println(string(bs))
```

- `io.Writer` interface used with `io.Reader` to pipe input to output with less code. Example `io.Copy`:
- `Writer()` function takes a `[]byte` slice as input and sends that data to a struct's output.

```Go
// Refactor above snippet
resp, _ := http.Get("https://google.com")

// os.Stdout implements the io.Writer interface (implements Write() method)
// Notice how resp.Body which is of type io.ReadCloser can be used in place of an io.Reader argument in function Copy. This is the flexibility of choosing structural typing (implicit implementation)
// io.ReadCloser has embedded interfaces io.Reader, io.Closer (superset) and can be substitute in-place of a plain io.Reader type.
io.Copy(os.Stdout, resp.Body)

// Signature of io.Copy
func io.Copy(dst io.Writer, src io.Reader) (written int64, err error)
```

- __Go type assertions:__ Syntax to explore if a __struct instance satisfies an interface__ and thus if it has __methods__ needed (reflection). Usually in these cases the argument concrete type (struct instance) is uknown but satisfies some other interface, so it can be passed as argument.

```Go
// Instance: dst, test if satisfies interface: ReaderFrom
// If ok is true then ReadFrom() must exist
if instance, ok := dst.(ReaderFrom); ok {
  return instance.ReadFrom(someValue)
}

// Type assertion
obj, isOfType := variable.(type)
```

#### Channels & Go Routines

- [https://www.atatus.com/blog/goroutines-error-handling/](https://www.atatus.com/blog/goroutines-error-handling/)
- A Go program consists of a __go routine__ running inside a process (the engine that executes code). So, go's `main()` is the single go routine that executes during program execution.
- `go` keyword in front of function call means run the function inside a new __go routine__ (spawn a new __child__ go routine __thread__), instead of waiting on a __blocking call.__
- By default: Go scheduler __tries to use 1 CPU core__ by running go routines one at a time, unless they finish or get to a __blocking call__ (idle/waiting) - __Asynchronous/Concurrent execution.__
- If we override the 1 CPU core setting with more, multiple go routines can be assigned on each core at the same time - __Parallel execution.__
- There is execution priority that favours __main__ go routine, to __child__ go routines.
  - __Gotcha:__ __main__ go routine finishesv(exits) before __child__ routines have finished. We have to make `main()` wait for results from child go routines.
  - We achieve this using __channels.__ Channels is the only __data type__ we have to communicate between go routines, including __main.__
- Buffered vs Unbuffered channels [https://medium.com/a-journey-with-go/go-buffered-and-unbuffered-channels-29a107c00268](https://medium.com/a-journey-with-go/go-buffered-and-unbuffered-channels-29a107c00268)
  - If the capacity is zero or absent, the channel is __unbuffered__ and communication succeeds only when __both a sender and receiver are ready.__
  - If the channel is __unbuffered__, the sender __blocks__ until the receiver has received the value. This is because effectively the channel has "no way" to __store messages inside__, for consumption.
  - In the case of __buffered__ channel, the size of the __buffer__, means __how many messages__ it can store. Essentially, senders __do not block, until a receiver has received the value__, or until the __channel buffer is full.__
  - __Under-sized buffers__ can impact performance, by incurring __latency,__ due to synchronization blocking, when the buffer is full.

- Sending - receiving data with channels

```Go
// Send value 4 into a channel
channel <- 4

// Wait to receive value from channel. When a value is sent, assign the value to myNum.
myNum <- channel

// Wait to receive value from channel.  When a value is sent, immediately pass to function argument.
fmt.Println(<-channel)
```

- Ways to block a channel - Channel gotchas

```Go
// Example of blocking unbuffered channel

package main

import (
  "fmt"
  "net/http"
  "time"
)

func checkLink(link string, c chan string) {
  // Blocking call
  _, err := http.Get(link)
  if err != nil {
    fmt.Println(link, "might be down!")
    c <- link
    return
  }

  fmt.Println(link, "is up!")
  c <- link
}

func main() {
  links := []string{
    "http://google.com",
    "http://facebook.com",
    "http://stackoverflow.com",
    "http://golang.org",
    "http://amazon.com",
  }

  // Allocate unbuffered channel
  c := make(chan string)

  for _, link := range links {
    go checkLink(link, c)
  }

  // Gotcha: Receiver is outside a for loop.
  // It will block (wait) until the first go routine finishes, and then will exit (it will print only 1 message)
  fmt.Println(<-c)

  // Gotcha: How to block a channel forever: Add more receivers (6) than senders (5)
  for i := 0; i < len(links); i++ {
    fmt.Println(<-c)
  }
  // This additional one will block, since there is no sender left.
  fmt.Println(<-c)

  // Proper loop: Receiver will have to wait for go routines to send in the channel, before print-outs.
  // Not all will need to finish, to start the print outs. But for the for loop to complete, all go routines, will have to have finished.
  // This for loop is essentially a repeated receiver, short of l <- c
  for l := range c {
    fmt.Println(l)
  }

  // Implement endless status checks without interval. First argument on checkLink is valid string (messages received from channel c)
  for {
    go checkLink(<-c, c)
  }
  // Alternative syntax - better idiomatic (explicit receive on channel)
  for l := range c {
    go checkLink(l, c)
  }

  // Implement endless status checks every 5 sec, using "endless" repeat receivers in anonymous function.
  // Simply receivers never finish, since new go routines (senders) push messages in the channel.
  // For loop never finishes.
  for l := range c {
    // Anonymous go routine (proper name: function literal). Immediately invoked function execution (IIFE)
    // Wrap sleep inside a go routine, to avoid blocking the main go routine.
    // While the main routine is paused, it cannot receive new messages. Messages are sent and queued.
    go func(link string) {
      // Sleep pauses the current go routine (anonymous)
      time.Sleep(5 * time.Second)
      checkLink(link, c)
    }(l)
  }

  // What if we used l receivers directly as closure.
  for l := range c {
    go func() {
      time.Sleep(5 * time.Second)
      checkLink(l, c)
    }()
  }

  // After the first run of the 5 links, the closure variable captures state of the last link visited.
  // In essence we pass a variable value to a go routine, that currently is maintained by another goroutine!
  // This means that repeated runs will check against the last captured url for 5 times, instead!
  // This happens because all go routines reference the same enclosed variable, from the outer scope (for range loop).
  // In order to resolve this, we pass the mutated l receiver as value (copies the value to each go routine inner scope).
}
```

> Note: __NEVER share (or reference) the same__ variable between different go routines.

### GRPC MAsterclass

- [https://www.udemy.com/course/grpc-golang](https://www.udemy.com/course/grpc-golang)

### Concurrency in GO

- [https://www.udemy.com/course/up-n-running-with-concurrency-in-golang](https://www.udemy.com/course/up-n-running-with-concurrency-in-golang)

### Go Serverless

- [https://www.udemy.com/course/hands-on-serverless-computing-with-go](https://www.udemy.com/course/hands-on-serverless-computing-with-go)

### Go Design Patterns

- [https://www.udemy.com/course/design-patterns-go](https://www.udemy.com/course/design-patterns-go)

#### SOLID Principles

- Single Responsibility Principle (SRP)
- Open-Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)

#### Builder Pattern

- Problem: Some Objects are simple and can be created in single constructor (or factory function) call
- Other objects require a lot of __ceremony to create.__
- Having a factory function with 10 arguments __is not productive, nor clean.__
- __Builder:__ an API for constructing an object step-by-step.
- Existing Builder pattern `strings.Builder` example:

```Go
import (
  "fmt"
  "strings"
)

func main() {
  hello := "hello"
  sb := strings.Builder{}
  sb.WriteString("<p>")
  sb.WriteString(hello)
  sb.WriteString("</p>")
  // Get concatenated (created) string
  fmt.Printf("%s\n", sb.String())

  // Alternative way to stringify a list of strings, other than join
  words := []string{"hello", "world"}
  sb.Reset()
  // Create unordered html list from a string slice
  // <ul><li>...</li><li>...</li><li>...</li></ul>'
  sb.WriteString("<ul>")
  for _, v := range words {
    sb.WriteString("<li>")
    sb.WriteString(v)
    sb.WriteString("</li>")
  }
  sb.WriteString("</ul>")
  fmt.Println(sb.String())
}
```

- Go __fluent interface__ - method that returns the receiver, so the user can chain calls [Builder](./go-design-patterns/builder/creational.builder.builder.go)

```Go
func (b *HtmlBuilder) AddChildFluent(
  childName, childText string) *HtmlBuilder {
  e := HtmlElement{childName, childText, []HtmlElement{}}
  b.root.elements = append(b.root.elements, e)
  return b
}

// Use it as follows
  b.AddChildFluent("li", "hello").AddChildFluent("li", "world")
  fmt.Println(b.String())
```

- __Builder Facets (multiple builders for single object)__ pattern ends up in a small __DSL__
- __Facets__ work by leveraging __embedding__ to switch from one builder to another, in a single __fluent interface__ [Builder Facets](./go-design-patterns/builder/creational.builder.builderfacets.go)
- __Best-practice: Hide__ the actual object (struct) by making it private (lowercase) and export the builder externally (uppercase) [Parameter](./go-design-patterns/builder/creational.builder.builderparameter.go)
- __Functional Builder__ [Functional Builder](./go-design-patterns/builder/creational.builder.functionalbuilder.go) __simplifies__ a lot of the code of builder methods, by keeping a list of build actions inside the builder.

```Go
type Person struct {
  name, position string
}

type personMod func(*Person)
type PersonBuilder struct {
  actions []personMod
}

func (b *PersonBuilder) Called(name string) *PersonBuilder {
  // Append a function literal to the actions slice
  b.actions = append(b.actions, func(p *Person) {
    p.name = name
  })
  return b
}

// Apply all functions to an empty Person object and return it
func (b *PersonBuilder) Build() *Person {
  p := Person{}
  for _, a := range b.actions {
    a(&p)
  }
  return &p
}

// Dynamic Extensibility - OCP
func (b *PersonBuilder) WorksAsA(position string) *PersonBuilder {
  b.actions = append(b.actions, func(p *Person) {
    p.position = position
  })
  return b
}

func main() {
  b := PersonBuilder{}
  p := b.Called("Dmitri").WorksAsA("dev").Build()
  fmt.Println(*p)
}
```

#### Factory Pattern

- __Problem:__ Object creation becomes convoluted, we want to return different concrete objects that satisfy an interface, conditionally or business logic encapsulation on initializing of fields.
- __Wholesale__ object creation - the inverse of __piecewise creation__ of Builder. Factory creates a whole full object, in one single invocation.
  - __Factory function__ aka Constructor
  - Separate struct - called __Factory__
  - __Factory Generator__

- Factory function that returns an __interface__ of concrete (hidden implementation) structs

```Go
// Hide concrete person as private
type person struct {
  name string
  age int
}

type tiredPerson struct {
  name string
  age int
}

// Expose the interface
type Person interface {
  SayHello()
}

func (p *person) SayHello() {
  fmt.Printf("Hi, my name is %s. I am %d years old.\n", p.name, p.age)
}

func (p *tiredPerson) SayHello() {
  fmt.Println("Sorry I'm too tired.")
}

// Expose the factory function. Since we return an interface, there is no need for *Person type.
// But we do return a pointer to the concrete object.
func NewPerson(name string, age int) Person {
  // Conditional logic that can return different concrete objects that satisfy the Person interface
  if age > 100 {
    return &tiredPerson{name, age}
  }
  return &person{name, age}
}

func main() {
  // Encapsulate name, age as private variables
  p := NewPerson("James", 34)
  p.SayHello()

  // This is illegal if used on another package
  p.name := "John"
}
```

- [__Factory Generator (Abstract Factory)__](./go-design-patterns/factory/creational.factories.factorygenerator.go)
  - Functional approach - factories as functions - cannot mutate factory fields after creation (more Go idiomatic, also popular pattern in Javascript)
  - Structural approach - factories as structs - can mutate factory fields after creation

```Go
// Functional Approach

type Employee struct {
  Name, Position string
  AnnualIncome   int
}

// what if we want factories for specific roles?

// functional approach - return a function for partial application - use only employee name as argument to the final factory.
func NewEmployeeFactory(position string, annualIncome int) func(name string) *Employee {
  return func(name string) *Employee {
    return &Employee{name, position, annualIncome}
  }
}

func main() {
  developerFactory := NewEmployeeFactory("developer", 80000)
  managerFactory := NewEmployeeFactory("manager", 100000)

  developerNames := []string{"John", "James", "Tom"}
  managerNames := []string{"Anna", "Lisa"}
  developers := make([]string, 0)
  managers := make([]string, 0)

  // Make similar employee objects in bulk
  for _, n := range developerNames {
    developers = append(developers, developerFactory(n))
  }

  for _, n := range managerNames {
    managers = append(managers, managerFactory(n))
  }
}
```

```Go
// Structural Approach
type Employee struct {
  Name, Position string
  AnnualIncome   int
}

type EmployeeFactory struct {
  Position string
  AnnualIncome int
}

func (f *EmployeeFactory) Create(name string) *Employee {
  return &Employee{name, f,Position, f.AnnualIncome}
}

// structural approach - return an EmployeeFactory
func NewEmployeeFactory(position string, annualIncome int) *EmployeeFactory {
  return &EmployeeFactory{position, annualIncome}
}

func main() {
  developerFactory := NewEmployeeFactory("developer", 80000)
  managerFactory := NewEmployeeFactory("manager", 100000)

  developerNames := []string{"John", "James", "Tom"}
  managerNames := []string{"Anna", "Lisa"}
  developers := make([]string, 0)
  managers := make([]string, 0)

  for _, n := range developerNames {
    developers = append(developers, developerFactory.Create(n))
  }

  for _, n := range managerNames {
    managers = append(managers, managerFactory.Create(n))
  }
}
```

- [__Prototype Factory__](./go-design-patterns/factory/creational.factories.protofactory.go) - Related also to __Prototype__ Design Pattern

#### Prototype

- __Problem:__ Complicated objects aren't designed from scratch. They reiterate __existing designs.__
- An existing design (partially or fully constructed) is a __Protorype__
- We make a __copy (clone) of the prototype__ and customize it.
  - Requires __deep copy__ support, which means copy all elements as values, not copy pointers.
- We make the __cloning convenient__ (e.g. via a Factory)
- Tom implement a prototype
  - 1. __Partially construct__ an object and store it
  - 2. Deep copy the __prototype__
  - 3. __Customize__ the resulting instance
  - 4. __A Prototype Factory__ provides a convenient API for using prototypes.

- [__Deep Copy vs Shallow Copy Showcase__](go-design-patterns/prototype/creational.prototype.deepcopy.go) - manual method does not scale well when objects are complicated.
- [__Copy Method__](go-design-patterns/prototype/creational.prototype.copymethod.go) - helper `copy` built-in for slices:
  - The `copy` built-in function copies elements from a source slice into a destination slice. (As a special case, it also will copy bytes from a string to a slice of bytes.) The source and destination may overlap. Copy returns the number of elements copied, which will be the minimum of len(src) and len(dst).
  - __Copy method__ does not solve the problem of types you do not own.
- [__Copy through Serialization__](go-design-patterns/prototype/creational.prototype.serialization.go) - serialization to e.g. binary or json from/to struct is clever enough to achieve the deep copy outcomes (save/load all of its state).
- [__Prototype Factory](go-design-patterns/prototype/creational.prototype.factory.go) - eliminate the code in initializing structs, by providing factory methods with __pre-filled prototypes.__
  - Simply a prototype factory method, takes a prototype as argument, filled up with common fields values, deep copies it (creation of prototypes can be functions or structs), and implements the __customization__ by passing the arguments, to the customizable fields.

#### Singleton

- __Problem:__ For some components it makes sense to have only __one__ instance in the system.
  - Example: Database repository
  - Object factory
  - E.g. the construction call is expensive (resource-wise)
- We only create one instance
- We give everyone the same instance
- Prevet anyone creating additional copies - we create a private `struct` type and expose the `instance` publicly. Also use package `sync` with `sync.Once.Do()` struct (includes a `Mutex` field) & keep pointer to the one instance.
- Need to take care of __lazy instantiation__, only create the instance, when it is needed.
- [go-design-patterns/singleton/singleton.go](go-design-patterns/singleton/singleton.go)

- Singleton is considered an anti-pattern or design smell - breaks __DIP__ principle.
  - A usual side-effect of breaking __DIP__: __cannot create mocks__, will have to test on live data. Example: cannot assert number of results or values on live database, since data is always changing.
  - __Solution:__ Introduce an interface, mock the singleton and functions can depend on interface (implemented only by singleton on live code, implemented by mock on test code)

### Go Rest Microservices

- [https://www.udemy.com/course/rest-based-microservices-api-development-in-go-lang](https://www.udemy.com/course/rest-based-microservices-api-development-in-go-lang)

## Configuration & VSCode issues

- Any Go package, needs `go mod init` when using `go1.15+`. This resolves `undeclared name` errors with code not using modules.
- To resolve the VsCode `gopls` issue with __multiple modules per workspace folder__ (stable version does not allow multiple modules in a single folder under a `.vscode` workspace) add the following configuration to __workspace__ `settings.json`

```JSON
"gopls": {
  "experimentalWorkspaceModule": true,
}
```

## Interesting SO Questions

- [Named Function Arguments](https://stackoverflow.com/questions/23447217/go-named-arguments) - Fo refactor reasons, it's always better to refactor long lists of arguments with __structs__
- [No default values/method overloading supported](https://stackoverflow.com/questions/2032149/optional-parameters-in-go)

```Go
// Go supports pack/unpack functions that accept/return the same argument signatures

// Args returns 3 int values
func Args() (a int, b int, c int) {
    return 1,2,3
}

// Bar accepts 3 int parameters
func Bar(a,b,c int) {
    fmt.Println(a,b,c)
}

// Unpack Args inside Bar call - supported
func main() {
    Bar(Args())
}
```

## Notes from `koslib`

- Avoid different variable names, opt for `err` (mutations isn't really a problem)
- When __single__ binary - use repo name `cmd/reponame` package name, by convention
- `config` antipattern - move to `cmd/<name>/init*.go` files with init functions (not auto `init()` func in `main.go`), that receive configuration details (e.g. from environment vars) & separate `config.go` with configuration constant, or variable __declarations only__. Example:

```Shell
# cmd high-level package
cmd
|__<repo-name> # produces binary <repo-name>
  |__main.go
  |__initEnv.go # import config to set variables, structs
  |__initDB.go # import config to set variables, structs
# config high-level package
config
|__config.go # var, const, struct declarations only of configuration values.
```

- Also, avoid using `init()` auto-init fuction in `main.go`, since it can have a lot of initialization __magic__ with unintended consequences. Prefer to use `init*` function calls, by functionality, sequentially, for stablitity reasons.
- Avoid using `pkg` or `internal` on small/medium projects, packages in root folder per functionality & `cmd` package is a good practice. If package explosion is real then use some ideas from [https://github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout) although it's __not an official standard.__
- __Good practice:__ Expose only interfaces, leave __implementations private__.
- __Good practice:__ Structs with receivers can go to their own sub-package, based on functionality. Don't put all related structs on the same file.
- __Opinionated good practice:__ Separate interfaces from concrete implementation, to different files, by utilizing sub-packages. Example:

```Shell
# High-level package name
persistence
|__repository.go # interface goes there
|__postgresql # sub-package
   |__repository.go # concrete implementation
   |__connector.go # helpers of concrete implementation
```

- Package structure for web services:
  - `api`: Contains routes (urls) only separated from their handlers (views/controllers) to different files. If api structure is complicated, split up between `api` and `handlers` packages.
  - `service`: Contains business delegation logic, between api and persistence. Do the delegation and orchestraton there, do not include everything. Separate to different packages, per functionality.
  - `models`: Data persistence models.
  - Example:

```Shell
api # api high-level package
|__handlers.go # handlers only
|__routes.go # urls only
|__middleware.go # do something intermediate with request/response processing, e.g. handle headers etc.
```
