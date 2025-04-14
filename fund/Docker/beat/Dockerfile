#!/bin/bash

# docker build --tag fund_beat .
# docker run -d -v /Users/chenhaiou/Desktop/D/git/fund:/usr/src/app/fund --name fund_beat fund_beat

FROM python:3.8.9

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD celery -A fund.fund_celery beat
