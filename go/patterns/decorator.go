package main

import (
	"fmt"
)

type someFunc func(s string)

func decorate(f someFunc) someFunc {
	return func(s string) {
		fmt.Println("Doing something before...")
		f(s)
		fmt.Println("Doing something after...")
	}
}

func displayText(s string) {
	fmt.Println(s)
}

func main() {
	display := decorate(displayText)
	display("Client code")
}

// OUTPUT
// Doing something before...
// Client code
// Doing something after...
