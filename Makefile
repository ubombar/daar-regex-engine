build:
	go mod tidy
	go test ./...
	go build -o bin/egrep main.go 

run:
	./bin/egrep
