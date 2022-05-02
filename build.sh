#!/bin/sh
cdir=.
dist=$cdir/static/dist
image=fastapi/imagename
npmimg=fastapi/npm
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
    docker build -f $cdir/dockerfile_fastapi --target $taget -t $image $cdir
    appid=$(docker images -q $image)
    if [ ! -z "$appid" ]
    then        
        echo "Image Name = $image, Image ID = $appid"
        cat docker.hub.txt | docker login -u haan78 --password-stdin
        docker image tag $image:latest haan78/baris:$image
        dhash=$(docker image push -q haan78/baris:$image)
        docker logout
        if [ ! -z "$dhash" ]
        then
            echo "image is ready"
            exit 0
        else
            echo "Image upload error"
        fi
    else
        echo "Application image can't create"
    fi
else
    echo "Dist folder can't create"    
fi
exit 1
