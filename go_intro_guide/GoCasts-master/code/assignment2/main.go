package main

import "fmt"

type shape interface {
	getArea() float64
}

type triangle struct {
	height float64
	base   float64
}

type square struct {
	sideLength float64
}

func main() {
	tr := triangle{
		height: 1.2,
		base:   2.2,
	}

	sq := square{sideLength: 1.3}

	fmt.Println("Triangle")
	printArea(tr)
	fmt.Println()

	fmt.Println("Square")
	printArea(sq)
	fmt.Println()
}

func (t triangle) getArea() float64 {
	return t.base * t.height * 0.5
}

func (s square) getArea() float64 {
	return s.sideLength * s.sideLength
}

func printArea(s shape) {
	area := s.getArea()
	fmt.Printf("Area is: %f\n", area)
}
