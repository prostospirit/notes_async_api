# pull official base image
FROM python:3.11-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean \
  && pip3 install poetry

# install python dependencies
COPY pyproject.toml /usr/src/app/
COPY poetry.lock /usr/src/app

RUN set -ex && poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

# add app
COPY migrations .

COPY docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh
RUN chmod +x /usr/src/app/docker-entrypoint.sh

