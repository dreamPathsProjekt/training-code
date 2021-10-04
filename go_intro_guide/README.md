# Go Introductory Guide - Best Practices

## Resources

- [https://github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout)
- [https://golang.org/doc/faq](https://golang.org/doc/faq)
- [https://golang.org/doc/effective_go](https://golang.org/doc/effective_go)
- Google Wire for DI on complicated projects
  - [https://github.com/google/wire/blob/main/_tutorial/README.md](https://github.com/google/wire/blob/main/_tutorial/README.md)
  - [https://go.dev/blog/wire](https://go.dev/blog/wire)

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

#### Channels & Go Routines

### GRPC MAsterclass

- [https://www.udemy.com/course/grpc-golang](https://www.udemy.com/course/grpc-golang)

### Go Serverless

- [https://www.udemy.com/course/hands-on-serverless-computing-with-go](https://www.udemy.com/course/hands-on-serverless-computing-with-go)

### Go Design Patterns

- [https://www.udemy.com/course/design-patterns-go](https://www.udemy.com/course/design-patterns-go)

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
