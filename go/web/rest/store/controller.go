package store

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

type Controller struct {
	Repository Repository
}

func (c *Controller) GetClients(w http.ResponseWriter, r *http.Request) {
	clients := c.Repository.GetClients()
	json.NewEncoder(w).Encode(clients)
}

func (c *Controller) AddClient(w http.ResponseWriter, r *http.Request) {
	var client Client
	_ = json.NewDecoder(r.Body).Decode(&client)
	c.Repository.AddClient(client)
	json.NewEncoder(w).Encode(client)
}

func (c *Controller) GetClient(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	clientId := params["id"]
	result := c.Repository.GetClientById(clientId)
	json.NewEncoder(w).Encode(result)
}

func (c *Controller) DeleteClient(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	clientId := params["id"]
	result := c.Repository.DeleteClient(clientId)
	json.NewEncoder(w).Encode(result)
}

func (c *Controller) UpdateClient(w http.ResponseWriter, r *http.Request) {
	var client Client
	_ = json.NewDecoder(r.Body).Decode(&client)
	c.Repository.UpdateClient(client)
	json.NewEncoder(w).Encode(client)
}
