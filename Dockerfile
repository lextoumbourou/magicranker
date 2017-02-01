FROM ubuntu:16.04

MAINTAINER Lex Toumbourou "lextoumbourou@gmail.com"

RUN apt-get update
RUN apt-get install -y libpq-dev libcurl4-openssl-dev python-dev python-pip python-virtualenv nodejs npm postgresql-client

RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g less
RUN npm install -g bower

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code
