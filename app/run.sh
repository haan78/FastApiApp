#!/bin/sh
while :
do
    echo "Starting UVICORN..."
	uvicorn --port=8001 --host=0.0.0.0 --reload main:APP
    echo "Waiting 5 Seconds..."
	sleep 5
done