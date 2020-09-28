package main

import (
	"./server"
)

func main() {
	gSvr := server.New()
	gSvr.Listen()
}
