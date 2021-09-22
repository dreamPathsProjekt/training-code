# Go Introductory Guide - Best Practices

## Resources

- [https://github.com/golang-standards/project-layout](https://github.com/golang-standards/project-layout)

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

### GRPC MAsterclass

- [https://www.udemy.com/course/grpc-golang](https://www.udemy.com/course/grpc-golang)

### Go Serverless

- [https://www.udemy.com/course/hands-on-serverless-computing-with-go](https://www.udemy.com/course/hands-on-serverless-computing-with-go)

## Configuration & VSCode issues

- Any Go package, needs `go mod init` when using `go1.15+`. This resolves `undeclared name` errors with code not using modules.
- To resolve the VsCode `gopls` issue with __multiple modules per workspace folder__ (stable version does not allow multiple modules in a single folder under a `.vscode` workspace) add the following configuration to __workspace__ `settings.json`

```JSON
"gopls": {
  "experimentalWorkspaceModule": true,
}
```
