# Implementation of PSA scheme using key-homomorphic PRFs.

## How to run the code
1. Install Go
2. Clone repository
3. Download dependencies
4. Run test code
5. (Create the plots)

### Install Go
Follow these [instructions](https://golang.org/doc/install) to download and install Go.
For our experiments we used go1.16.4 linux/amd64

### Clone repository
Clone this repository e.g. by executing in a terminal `git clone https://github.com/johanernst/khPRF-PSA.git`

### Download dependencies
Run in a terminal
`go get github.com/fentec-project/gofe/data`,
`go get github.com/fentec-project/gofe/sample` and
`go get golang.org/x/crypto/sha3`

We use gofe/data mainly for the vector datatypes and gofe/sample to create random vectors. For gofe/data and gofe/sample we used the git commit [6c325c8](https://github.com/fentec-project/gofe/commit/6c325c89872bc5e1be945a06f1dddec43c169759).

### Run test code
Run in a terminal
`./benchmark.sh` to run the performance test, or
`go test -run=TestDemo` for a short demo.
The benchmark program contains quite many pauses to avoid that processor overheating influences the results. Therefore running `./benchmark.sh` will take several hours. Feel free to reduce the pauses or the number of iterations in \"benchmark.sh\" and \"psa_test.go\".

### Create the plots
When you executed `./benchmark.sh` there will be a file \"runtime.txt\". This file contains the benchmark results. Executing `python3 plot.py` will create plots and print exact running times (and standard deviation) for 1000, 5000 and 10000 users.
