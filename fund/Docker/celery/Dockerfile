#!/bin/bash

# docker build --tag fund_celery .
# docker run -d -v /Users/chenhaiou/Desktop/D/git/fund:/usr/src/app/fund --name fund_celery fund_celery
# celery -A fund.fund_celery worker

FROM python:3.8.9

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD celery -A fund.fund_celery worker
