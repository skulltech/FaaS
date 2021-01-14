FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

COPY ./app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /var/lib/filer
ENV STORAGE_DIRECTORY="/var/lib/filer"

COPY ./app /app
