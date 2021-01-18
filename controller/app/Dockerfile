FROM python:3
ARG payload

RUN mkdir -p /app
RUN curl -sL $payload -o /app/payload.zip
COPY run.py /app

WORKDIR /app
RUN unzip -o payload.zip
RUN pip3 install -r requirements.txt
