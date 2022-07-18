FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY apks.py /app/apks.py
COPY cron /app/cron
COPY requirements.txt requirements.txt

RUN touch /app/apks.log
RUN touch /app/result.csv

RUN pip3 install -r requirements.txt

RUN apk update && apk upgrade
RUN chmod +x apks.py

RUN crontab /app/cron

#CMD crond && tail -f /app/apks.log
#CMD crond && tail -f /app/result.csv