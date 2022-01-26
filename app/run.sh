#!/bin/sh

P=$(netstat -lntu | grep LISTEN | awk '{ print $4 }' | grep 0.0.0.0 | awk '{ split($0,a,":"); print a[2] }')
while :
do
    if [ ! -z "$P" ]
    then
        echo "Starting UVICORN with port $P"
        uvicorn --port=$P --host=0.0.0.0 --reload main:APP
    else
        echo "There is no availible port"
        uvicorn --port=8001 --host=0.0.0.0 --reload main:APP
    fi	
    echo "Waiting 5 Seconds..."
	sleep 5
done

