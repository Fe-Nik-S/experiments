package store

type Repository struct{}

var clients = Clients{}

func (r Repository) GetClients() Clients {
	return clients
}

func (r Repository) GetClientById(id string) Client {
	for _, item := range clients {
		if item.ID == id {
			return item
		}
	}
	return Client{}
}

func (r Repository) AddClient(client Client) bool {
	clients = append(clients, client)
	return true
}

func (r Repository) UpdateClient(client Client) bool {
	for index, item := range clients {
		if item.ID == client.ID {
			clients[index] = client
			return true
		}
	}
	return true
}

func (r Repository) DeleteClient(id string) bool {
	for index, item := range clients {
		if item.ID == id {
			clients = append(clients[:index], clients[index+1:]...)
			return true
		}
	}
	return true
}
