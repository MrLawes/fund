#!/bin/bash

# docker build --tag fund_runserver .
# docker run -d -v /Users/chenhaiou/Desktop/D/git/fund:/usr/src/app/fund --name fund_runserver -p 10001:10001 fund_runserver

FROM python:3.8.9

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD python /usr/src/app/fund/manage_test.py runserver 0.0.0.0:10001
