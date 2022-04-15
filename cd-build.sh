#!/bin/sh
wd=$(pwd)
imageprefix="fastapiapp"
port=8001
version=1.0

docker build -f $wd/dockerfile_npm --target production -t $fastapiapp/npm:$version $wd
docker run -ti -v $wd/static:/static:consistent $fastapiapp/npm
docker build -f $wd/dockerfile_fastapi --target production -t $fastapiapp/runner:$version $wd

docker run -ti -p $port:8001 $fastapiapp/runner:$version