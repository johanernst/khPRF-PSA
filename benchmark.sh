#/bin/bash

for ((j = 0 ; j < 5 ; j=$j+1)); do
    for ((i = 1000 ; i < 10001 ; i=$i+1000)); do
	    go test -run=TestRuntime -args $i
	    sleep 120
    done
    sleep 180
done
