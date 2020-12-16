FROM python:3
ARG payload

RUN mkdir -p /app
COPY $payload /app
COPY run.py /app

WORKDIR /app
RUN unzip -o $(basename $payload)
RUN pip3 install -r requirements.txt
