FROM python:3
ARG payload
RUN test -n $payload

RUN mkdir -p /app
COPY $payload /app
COPY run.py /app

WORKDIR /app
RUN unzip -o $payload
RUN rm $payload
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "run.py" ]
