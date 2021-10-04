package main

import (
	"io"
	"log"
	"os"
)

func main() {
	filename := os.Args[1]
	f, err := os.Open(filename)
	if err != nil {
		log.Fatalf("unable to open file %s. %v\n", filename, err)
	}

	io.Copy(os.Stdout, f)
}
