FROM postgres:latest

COPY .env /tmp/.env

RUN cat /tmp/.env >> /etc/environment

ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

EXPOSE 5432

FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-pip

RUN pip install poetry

WORKDIR /app
COPY . /app

RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

