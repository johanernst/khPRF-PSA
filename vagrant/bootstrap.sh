#!/usr/bin/env bash

sudo apt-get update

#install golang
wget -q https://golang.org/dl/go1.16.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.16.5.linux-amd64.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> /home/vagrant/.profile
export PATH=$PATH:/usr/local/go/bin

#clone git repo
git clone https://github.com/johanernst/khPRF-PSA.git
sudo chown -R vagrant khPRF-PSA/

#install go dependencies
go get github.com/fentec-project/gofe/data
go get github.com/fentec-project/gofe/sample
go get golang.org/x/crypto/sha3

#install matplotlib for the python script
sudo apt-get -y install python3-pip
pip3 install matplotlib
