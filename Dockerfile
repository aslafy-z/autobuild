FROM python:alpine

WORKDIR /app

COPY ./requirements.txt /app/

RUN apk add --no-cache --virtual .build-deps g++ musl-dev
RUN pip install -r requirements.txt
RUN apk del .build-deps

COPY app.py /app/

ENTRYPOINT ["/app/app.py"]
