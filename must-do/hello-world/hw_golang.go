package main

import (
    "fmt";
    "os"
)

func main() {
    if len(os.Args) == 1 {
        fmt.Println("Please, write your name as first argument of program.")
        return
    }

    name := os.Args[1]
    welcome_msg := get_welcome_message(name)
    fmt.Println(welcome_msg)
}

func get_welcome_message(name string) string {
    return fmt.Sprintf("Hello, world! I'm a %s", name)
}
