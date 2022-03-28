#!/bin/sh
cd /app

while :
do
    uvicorn --port=8001 --host=0.0.0.0 --reload main:APP
    sleep 3
done