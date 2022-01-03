#!/bin/sh

##BASEDIR="$( cd "$( dirname "$0" )" && pwd )"
BASEDIR=/docker-entrypoint-initdb.d

for file in `ls $BASEDIR/*.arc`
do
    dbname=$(basename -s .arc $file)    
    mongorestore --db=$dbname --drop --archive=$file -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin   
done