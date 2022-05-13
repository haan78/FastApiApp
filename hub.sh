#!/bin/sh

#gerekli tanimlamalar
imagename="fasvelte1"
dockerhubserver=""
dockeruser="haan78"
dockercluster="baris"
mode=staging

npmimg="$imagename/npm"
#mevcut klasor
cdir=$(pwd)
version=$(cat $cdir/version.txt)
dockeraccesstoken=$(cat $cdir/config/hidden/docker_hub_token.txt)

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
docker run -v $cdir/static:/app/static:rw --env SCRIPT=$mode $npmid $cdir

if [ ! -d "$cdir/static/dist" ]
then
    echo "Dist folder can't create"
    exit 1 
fi

#Artik npm imajina ihtiyac kalmadi
docker image rm $npmid

#Uygulama sunucusunu hazirla
docker build -f $cdir/DockerPy --build-arg MODE=$mode --build-arg VERSION=$version -t $imagename $cdir

imgid=$(docker images -q $imagename)
if [ -z "$imgid" ]
then
    echo "Application image($imagename) can't create"
    exit 1
fi

echo "Image Name = $imagename, Image ID = $imgid"

echo $dockeraccesstoken | docker login -u $dockeruser --password-stdin $dockerhubserver
docker image tag $imagename:latest $dockeruser/$dockercluster:$imagename
dhash=$(docker image push -q $dockeruser/$dockercluster:$imagename)
docker logout

if [ -z "$dhash" ]
then
    echo "Image upload problem!!!"
    exit 1
fi

clear
echo "Looks good! Deployment steps on application server should be like these"
echo "Step 1: docker login -u [USERNAME] -p [PASSWORD] $dockerhubserver"
echo "Step 2: docker pull $dockeruser/$dockercluster:$imagename"
echo "Step 3: docker logout"
echo "Step 4: docker run -d -p [LOCAL]:[CONTAINER] $imagename"

exit 0

