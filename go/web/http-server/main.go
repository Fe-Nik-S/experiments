package main

import (
	"fmt"
	"html/template"
	"net/http"
)

type httpHandler struct {
	template string
}

func (handler httpHandler) ServeHTTP(response http.ResponseWriter, req *http.Request) {
	fmt.Fprint(response, handler.template)
}

type ViewData struct {
	Title       string
	Description string
	Users       []User
}

type User struct {
	Name    string
	Age     int
	Visible bool
}

func main() {

	const address string = ":8080"

	fileServer := http.FileServer(http.Dir("static"))
	http.Handle("/", fileServer)

	http.HandleFunc("/home", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Home page")
	})

	aboutHandler := httpHandler{template: "About"}
	http.Handle("/about", aboutHandler)

	data := ViewData{
		Title:       "Users List",
		Description: "Users List",
		Users: []User{
			User{Name: "Xander", Age: 15, Visible: true},
			User{Name: "Katy", Age: 20, Visible: false},
			User{Name: "Penny", Age: 32, Visible: true},
		},
	}
	http.HandleFunc("/users", func(w http.ResponseWriter, r *http.Request) {
		tmpl, _ := template.ParseFiles("templates/users.html")
		tmpl.Execute(w, data)
	})

	fmt.Println(fmt.Sprintf("Server is listening 127.0.0.1%s...", address))
	fmt.Println(fmt.Sprintf("Existing methods:\n   /about\n   /home\n   /users"))

	http.ListenAndServe(address, nil)
}
