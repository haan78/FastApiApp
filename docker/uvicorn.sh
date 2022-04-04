#!/bin/sh
cd /app

MODE=$(printenv MODE)

prm="--port=8001 --host=0.0.0.0 --reload"

if [ "$MODE" == "dev" ]
then
    echo "Runing in development mode"
    prm="--reload ""$prm"
else
    echo "Runing in production mode"
fi
uvicorn $prm main:APP