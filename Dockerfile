FROM python:3.7-alpine AS base

RUN \
 apk add --no-cache --virtual=build-dependencies \
    autoconf \
    automake \
    g++ \
    gcc \
    linux-headers \
    make \
    openssl-dev \
    zlib-dev

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.7-alpine

COPY --from=base /install /usr/local
COPY exporter /exporter

WORKDIR /exporter

ENTRYPOINT ["python", "/exporter/exporter.py"]
