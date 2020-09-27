package main

import (
	"context"
	"fmt"
	"os"
	 pb "../pb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/grpclog"
)

func main() {
	opts := []grpc.DialOption{
		grpc.WithInsecure(),
	}
	conn, err := grpc.Dial("127.0.0.1:5500", opts...)
	if err != nil {
		grpclog.Fatalf("fail to dial: %v", err)
	}
	defer conn.Close()

	args := os.Args
	if len(args) < 2 {
		grpclog.Fatalf("Please specify name as second argument...")
	}
	client := pb.NewGreeterClient(conn)
	request := &pb.HelloRequest{
		Name: args[1],
	}
	response, err := client.SayHello(context.Background(), request)
	if err != nil {
		grpclog.Fatalf("fail to dial: %v", err)
	}
   fmt.Println(response.Message)
}
