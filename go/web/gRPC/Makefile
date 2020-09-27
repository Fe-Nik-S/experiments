
init_env:
	go get github.com/golang/protobuf/proto
	go get google.golang.org/grpc
	go get google.golang.org/grpc/codes
	go get google.golang.org/grpc/status

build:
	CGO_ENABLED=0 go build main.go

image_build:
	docker build -t go-grpc .

image_run:
	docker run -it -p 5500:5500 go-grpc
