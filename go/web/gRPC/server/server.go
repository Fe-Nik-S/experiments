package server

import (
	"context"
	"fmt"
	"log"
	"net"

	pb "../pb"
	"google.golang.org/grpc"
)

type Greeter struct {}

func New() *Greeter {
	return &Greeter{}
}

func (g *Greeter) Listen() error {
	log.Println("Server is starting...")
	listener, err := net.Listen("tcp", ":5500")
	if err != nil {
		return err
	}
	log.Println("Server is ready...")
	grpcServer := grpc.NewServer()
	pb.RegisterGreeterServer(grpcServer, g)
	grpcServer.Serve(listener)
	return nil
}

func (g *Greeter) SayHello(ctx context.Context, r *pb.HelloRequest) (*pb.HelloResponse, error) {
	log.Println(fmt.Sprintf("Server executed request/hello-request: {name: %s}...", r.Name))
	return &pb.HelloResponse{
		Message: fmt.Sprintf("Hello, %s!", r.Name),
	}, nil
}
