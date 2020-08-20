FROM python:3.8.5-slim

RUN apt update && \
    apt install -y python-scrapy

RUN mkdir -p /app
WORKDIR /app

