#!/bin/bash

# docker build --tag fund_celery .
# docker run -d -v /Users/chenhaiou/Desktop/D/git/fund:/usr/src/app/fund --name fund_celery -p 10002:10002 fund_celery
# celery -A fund.fund_celery  worker --loglevel=info  -Q fund_celery

FROM python:3.8.9

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD python /usr/src/app/fund/manage_test.py runserver 0.0.0.0:10002
