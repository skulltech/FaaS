FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps build-base mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps

COPY ./app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV DOCKER_SERVER="hal9011"

COPY ./app /app
