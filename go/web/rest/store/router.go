package store

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

var routes = Routes{
	Route{
		Name:        "GetClients",
		Method:      "GET",
		Pattern:     "/clients",
		HandlerFunc: controller.GetClients,
	},
	Route{
		Name:        "GetClient",
		Method:      "GET",
		Pattern:     "/clients/{id}",
		HandlerFunc: controller.GetClient,
	},
	Route{
		Name:        "AddClient",
		Method:      "POST",
		Pattern:     "/clients",
		HandlerFunc: controller.AddClient,
	},
	Route{
		Name:        "UpdateClient",
		Method:      "PUT",
		Pattern:     "/clients/{id}",
		HandlerFunc: controller.UpdateClient,
	},
	Route{
		Name:        "DeleteClient",
		Method:      "DELETE",
		Pattern:     "/clients/{id}",
		HandlerFunc: controller.DeleteClient,
	},
}

var controller = &Controller{Repository: Repository{}}

func NewRouter() *mux.Router {
	router := mux.NewRouter().StrictSlash(true)
	for _, route := range routes {
		var handler http.Handler
		log.Println("Added a new route: ", route.Method, route.Pattern)
		handler = route.HandlerFunc

		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}
	return router
}
