#!/bin/sh
cd /app

MODE=$(printenv MODE)

prm="--port=8001 --host=0.0.0.0 --reload"
app="main:APP"

if [ "$MODE" == "dev" ]
then
    echo "Runing in development mode"
    prm="--reload ""$prm"
    while :
    do
        uvicorn $prm $app
        sleep 2
    done
else
    echo "Runing in production mode"
    uvicorn $prm $app
fi

