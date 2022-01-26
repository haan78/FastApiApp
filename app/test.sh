#!/bin/sh

P=$(netstat -lntu | grep LISTEN | awk '{ print $4 }' | grep 0.0.0.0 | awk '{ split($0,a,":"); print a[2] }')
echo $P