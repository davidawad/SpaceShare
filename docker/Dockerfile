FROM python:3.6

MAINTAINER David Awad "davidawad64@gmail.com"

COPY . /spaceshare
WORKDIR /spaceshare

RUN pip install -r /spaceshare/requirements.txt

CMD python /spaceshare/server.py
