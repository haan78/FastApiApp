#!/bin/sh

#gerekli tanimlamalar
imagename="fasvelte1"
dockerhubserver=""
dockeruser=$1
dockeraccesstoken=$2
dockercluster=$3
mode=testdrive
scritp=staging

npmimg="$imagename/npm"
#mevcut klasor
cdir=$(pwd)
nevfile=$cdir/config/hidden/$mode.env
version=$(cat $cdir/version.txt)
#dockeraccesstoken=$(cat $cdir/config/hidden/docker_hub_token.txt)

if [ ! -f "$nevfile" -o ! -s "$nevfile" ]
then
    echo "ENV file not found or empty $nevfile"
    exit 1
elif [ -z "$dockeruser" ]
then
    echo "Docker Hub user is empty"
    exit 1
elif [ -z "$dockeraccesstoken" ]
then
    echo "Docker Hub AT is empty"
    exit 1
elif [ -z "$dockercluster" ]
then
    echo "Docker Hub cluster is empty"
    exit 1
fi

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
docker run -v $cdir/static:/app/static:rw --env SCRIPT=$scritp $npmid $cdir

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
docker image rm $imagename

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

