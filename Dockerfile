FROM python:3.11.0a3-alpine3.15 AS base
#RUN apk add --no-cache python3 py3-pip
#FROM alpine:20220328 AS base
ARG POTR=8001
ENV TZ=Turkey
RUN apk update \
    apk upgrade 
    
COPY ./backend /app/backend
COPY ./static /app/static
RUN pip install --upgrade pip\
    pip install --no-cache-dir -r /app/backend/piplist.txt

COPY ./frontend /app/frontend
RUN apk add --update npm
RUN npm --prefix /app/frontend install /app/frontend
EXPOSE $PORT

FROM base AS production
COPY ./config/staging.env /etc/app.env
WORKDIR /app/frontend
RUN npm run production
WORKDIR /app/backend
ENTRYPOINT python run.py staging $PORT

FROM base AS staging
COPY ./config/staging.env /etc/app.env
WORKDIR /app/frontend
RUN npm run staging
WORKDIR /app/backend
ENTRYPOINT python run.py staging $PORT


FROM base AS development
COPY ./config/development.env /etc/app.env
RUN apk add --no-cache supervisor
COPY ./config/supervisor.conf /etc/supervisor.conf
ENTRYPOINT supervisord -c /etc/supervisor.conf
