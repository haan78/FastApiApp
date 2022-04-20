#!/bin/sh
cdir=$(pwd)
dist=$cdir/static/dist
image=fastapi/imagename
npmimg=nobetyazici/npm
taget=staging

npmid=$(docker images -q $npmimg)

createnpmimg()
{
    docker build -f $cdir/dockerfile_npm --target $taget -t $npmimg $cdir
    npmid=$(docker images -q $npmimg)
    if [ -z "$npmid" ]
    then
        echo "NPM image can't create"
        exit 1
    fi
}

if [ -z "$npmid" ]
then
    createnpmimg
elif [ "$1" == "rebuild" ]
then
    docker image rm $npmid
    createnpmimg
fi

docker run -ti -v $cdir/static:/static:consistent $npmid $cdir
if [ -d "$dist" ]
then
    rm -rf $dist/*.html
    docker build -f $cdir/dockerfile_fastapi --target $taget -t $image $cdir    
    if [ ! -z "$appid" ]
    then
        echo $appid
        exit 0
    else
        echo "Application image can't create"
        exit 1
    fi
else
    echo "Dist folder can't create"
    exit 1
fi
