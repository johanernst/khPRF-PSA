# Implementation of PSA scheme using key-homomorphic PRFs.
This repository contains the source code and performance test results of the Private Stream Aggregation (PSA) scheme proposed in the paper [Private Stream Aggregation with Labels in the Standard Model](https://petsymposium.org/2021/files/papers/issue4/popets-2021-0063.pdf) (PoPETS 2021). The implementation uses a simple lattice based key-homomorphic pseudorandom function (PRF) which is mentioned on page 2 in [Key Homomorphic PRFs and Their Applications](https://eprint.iacr.org/2015/220.pdf). The PRF is secure in the random oracle under the learning with rounding errors (LWE) assumption. The source code of the PRF is in the \"prf\" folder. The source code of the PSA scheme is in the file \"psa.go\".

## How to download and run the code
The following instructions have been tested under Ubuntu 18.04 and Ubuntu 20.04.
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
* `go get github.com/fentec-project/gofe/data`
* `go get github.com/fentec-project/gofe/sample`
* `go get golang.org/x/crypto/sha3`

We use gofe/data mainly for the vector datatypes and gofe/sample to create random vectors. For gofe/data and gofe/sample we used the git commit [6c325c8](https://github.com/fentec-project/gofe/commit/6c325c89872bc5e1be945a06f1dddec43c169759).

### Run test code
Change directory to the repository with `cd khPRF-PSA`.
Then run in a terminal
`./benchmark.sh` to run the performance test, or
`go test -run=TestDemo` for a short demo.
The benchmark program contains quite many pauses to avoid that processor overheating influences the results. Therefore running `./benchmark.sh` will take several hours. Feel free to reduce the pauses or the number of iterations in \"benchmark.sh\" and \"psa_test.go\".

For running the benchmark the system should have 16GB of RAM. For the demo 1GB of free RAM is sufficient.


### Create the plots
This requires Python3 and the python library \"matplotlib\" to be installed.

In the \"data\" folder there are the files \"runtime.txt\" and \"runtime_lass.txt\" which contain the results of the performance tests of our scheme and LaSS respectively. Executing `python3 plot.py` will create the same plots as in our paper. Futhermore the script prints the average running times (and standard deviation) for 1000, 5000 and 10000 users of the encryption and decryption algorithm. These are the numbers that appear in Table 2 in the paper.
Executing `./benchmark.sh` will run the benchmark and append the result to \"runtime.txt\".
The python script will look for both \"runtime.txt\" and \"runtime_lass.txt\". If both are present, they must have the same length. If you run your own performance tests, its best to delete or rename both \"runtime.txt\" and \"runtime_lass.txt\" and then execute `./benchmark.sh`.

## How to run the code by using Vagrant
For running the benchmark inside the vagrant VM the system should have 16GB of RAM. For running the demo inside the VM the system should have 2GB of free RAM (ca. 1GB for vagrant and 1GB for the demo).

1. Install and set up [Vagrant](https://www.vagrantup.com/)
2. Clone this git repository or download the \"vagrant\" folder.
3. Run `vagrant up` inside the vagrant folder.
4. Run `vagrant ssh` to get into the vagrant VM.
5. Type `cd khPRF-PSA` and then `go test -run=TestDemo`.

In case you are having problems with `vagrant up`, [this stackoverflow thread](https://stackoverflow.com/questions/60350358/how-do-i-resolve-the-character-device-dev-vboxdrv-does-not-exist-error-in-ubu) might help. These are the commands that helped in my case (with VirtualBox already installed):
1. `sudo apt-get update`
2. `sudo apt-get install virtualbox-dkms`
3. `sudo apt install --reinstall linux-headers-$(uname -r) virtualbox-dkms dkms`
4. `sudo dpkg-reconfigure virtualbox-dkms`
5. `sudo dpkg-reconfigure virtualbox`
