#!/bin/sh

#gerekli tanimlamalar
imagename="projeadi"
dockerhubserver=""
dockeruser="haan78"
dockercluster="baris"

npmimg="$imageadi/npm"
#mevcut klasor
cdir=$(pwd)
version=$(cat "$cdir/version.txt")

#frontendi compile etmek icin npm i olustur
docker build -f $cdir/DockerNpm -t $npmimg $cdir
npmid=$(docker images -q $npmimg)
if [ -z "$npmid" ]
then
    echo "NPM image($npmimg) can't create"
    exit 1
fi

#Varsa mevcut dist'i silki kod eskide kalmasin
rm -rf /static/dist

#npm'i run et ve dist klasorunu tekrar olustur
docker run -v $cdir/static:/app/static:rw --env SCRIPT=staging $npmid $cdir

if [ ! -d "/static/dist" ]
then
    echo "Dist folder can't create"
    exit 1 
fi

#Artik npm imajina ihtiyac kalmadi
docker image rm $npmid

#Uygulama sunucusunu hazirla
docker build -f $cdir/DockerPy --build-arg MODE=staging --build-arg VERSION=$version -t $imagename $cdir

imgid=$(docker images -q $imagename)
if [ -z "$imgid" ]
then
    echo "Application image($imagename) can't create"
    exit 1
fi

echo "Image Name = $imagename, Image ID = $imgid"

cat $cdir/config/hidden/docker.hub.txt | docker login -u $dockeruser --password-stdin $dockerhubserver
docker image tag $imagename:latest $dockeruser/$dockercluster:$imagename
dhash=$(docker image push -q $dockeruser/$dockercluster:$image)
docker logout

if [ -z "$dhash" ]
then
    echo "Image upload problem!!!"
    exit 1
fi

echo "Image is ready"
echo "URL = $dockerhubserver/$dockeruser/$dockercluster:$imagename"
exit 0

