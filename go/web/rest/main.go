package main

import (
	"log"
	"net/http"

	"./store"
)

func main() {

	log.Println("Starting up...")

	router := store.NewRouter()

	log.Println("Server is listening ...")
	log.Fatal(http.ListenAndServe(":8080", router))
}
