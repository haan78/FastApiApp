
while :
do
    uvicorn --port=8001 --host=0.0.0.0 --reload --log-config=/etc/uvicorn_log.yml main:APP
    sleep 3
done