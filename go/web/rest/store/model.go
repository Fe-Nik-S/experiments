package store

type Client struct {
	ID        string    `json:"id,omitempty"`
	FirstName string    `json:"first_name,omitempty"`
	LastName  string    `json:"last_name,omitempty"`
	Contacts  *Contacts `json:"contacts,omitempty"`
}

type Contacts struct {
	Email string `json:"email,omitempty"`
	Phone string `json:"phone,omitempty"`
}

type Clients []Client
