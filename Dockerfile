#!/bin/bash

FROM python:3.8.9

WORKDIR /usr/src/app/fund

COPY requirements.txt /usr/src/app/fund

RUN pip install -r /usr/src/app/fund/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

#CMD ["export", 'DJANGO_SETTINGS_MODULE="settings"']

#CMD ["python", "manage_test.py", "runserver", "0.0.0.0:80"]

CMD ["uwsgi", "--ini", "uwsgi.ini"]
