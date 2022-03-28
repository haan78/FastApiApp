#!/bin/sh

cd /app
script=$(printenv script)

if [ ! -z "$script" ]
then
    echo "Command => npm run $script"
    npm run $script
else
    echo "Script must be set!"
    exit 1
fi
