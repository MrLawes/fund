#!/bin/bash

FROM python:3.8.9

RUN mkdir -p /var/log/supervisor/

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["uwsgi", "--ini", "uwsgi.ini"]
#
#CMD ["supervisord", "-n", '-c', "/usr/src/app/fund/supervisor.conf"]

#; supervisord -n -c  /usr/src/app/fund/supervisor.conf
