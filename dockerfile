FROM python:3.11.0a3-alpine3.15

WORKDIR /app

COPY piplist.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r piplist.txt

CMD [ "python", "./main.py" ]