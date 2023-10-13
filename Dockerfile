FROM postgres:latest

COPY .env /tmp/.env

RUN cat /tmp/.env >> /etc/environment

ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

EXPOSE 5432