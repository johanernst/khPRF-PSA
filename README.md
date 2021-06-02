# Implementation of PSA scheme using key-homomorphic PRFs.

## How to run the code
1. Install Go
2. Download dependencies
3. Run test code

### Install Go
Follow these [instructions](https://golang.org/doc/install) to download and install Go.

### Download dependencies
Run in a terminal
`go get github.com/fentec-project/gofe/data`
`go get github.com/fentec-project/gofe/sample`
`go get golang.org/x/crypto/sha3`

### Run test code
Run in a terminal
`./benchmark.sh` to run the performance test, or
`go test -run=TestDemo` for a short demo.
