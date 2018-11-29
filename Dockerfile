FROM python:3.6-alpine AS base

RUN \
 apk add --no-cache --virtual=build-dependencies \
    autoconf \
    automake \
    freetype-dev \
    g++ \
    gcc \
    jpeg-dev \
    lcms2-dev \
    libffi-dev \
    libpng-dev \
    libwebp-dev \
    linux-headers \
    make \
    openjpeg-dev \
    openssl-dev \
    tiff-dev \
    zlib-dev

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM python:3.6-alpine

COPY --from=base /install /usr/local
COPY exporter /exporter

WORKDIR /exporter

ENTRYPOINT ["python", "/exporter/exporter.py"]
