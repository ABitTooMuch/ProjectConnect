FROM python:3.6-alpine

RUN adduser -D projectconnect
RUN apk update && apk upgrade
RUN apk add --no-cache curl python pkgconfig python-dev openssl-dev libffi-dev musl-dev make gcc

WORKDIR /home/projectconnect

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN apk add libffi-dev
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY projectconnect.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP projectconnect.py

RUN chown -R projectconnect:projectconnect ./
USER projectconnect

EXPOSE 5000
ENTRYPOINT ["sh","boot.sh"]