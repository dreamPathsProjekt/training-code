package main

import "fmt"

func main() {
	var allDecimals []int

	for i := 0; i <= 10; i++ {
		allDecimals = append(allDecimals, i)
	}

	for _, num := range allDecimals {
		var output string
		if num%2 == 0 {
			output = "even"
		} else {
			output = "odd"
		}
		fmt.Printf("%d is %s\n", num, output)
	}
}
