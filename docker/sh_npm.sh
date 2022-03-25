#!/bin/sh

cd /app
script=$(printenv script)

if [ ! -z "$script" ]
then
    if [ ! -d "node_modules" ]
    then
        echo "NPM instalation has been started..."
        npm install
        if [ -d "node_modules" ]
        then
            echo "Command => npm run $script"
            npm run $script
        else
            echo "NPM instalation error"
            exit 1        
        fi
    fi
else
    echo "Script must be set!"
    exit 1
fi
