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

#### Variables/Functions

- Variables can be __initialized__ outside of a function, but cannot be __assigned__ a value. __No globals__ permitted.

### GRPC MAsterclass

- [https://www.udemy.com/course/grpc-golang](https://www.udemy.com/course/grpc-golang)

### Go Serverless

- [https://www.udemy.com/course/hands-on-serverless-computing-with-go](https://www.udemy.com/course/hands-on-serverless-computing-with-go)
