FROM ubuntu:14.04

MAINTAINER Lex Toumbourou "lextoumbourou@gmail.com"

RUN apt-get update
RUN apt-get install -y libpq-dev libcurl4-openssl-dev python-dev python-virtualenv

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD private.py /code/magicranker/_private.py
ADD . /code

EXPOSE 8000
