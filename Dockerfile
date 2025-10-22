FROM ghcr.io/astral-sh/uv:alpine3.22 AS base

LABEL maintainer="Jan Speckamp <j.speckamp@52north.org>" \
      org.opencontainers.image.authors="Jan Speckamp <j.speckamp@52north.org>" \
      org.opencontainers.image.url="https://github.com/52North/connected-systems-pygeoapi" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="52°North GmbH" \
      org.opencontainers.image.licenses="Apache 2.0" \
      org.opencontainers.image.ref.name="52north/connected-systems-pygeoapi" \
      org.opencontainers.image.title="52°North OGC API Connected Systems" \
      org.opencontainers.image.description="Implementation of OGC API Connected Systems"


# alpine is confused where to look for python libraries so we need to support it here
# ENV PYTHONPATH=/usr/lib/python3.12/site-packages
ENV PROJ_DIR=/usr
ENV PYTHONUNBUFFERED=1
# ENV UV_COMPILE_BYTECODE=1

RUN apk update
RUN apk add gcc g++ musl-dev gdal-dev python3-dev git proj proj-dev proj-util geos geos-dev py3-numpy py3-shapely py3-shapely-pyc

WORKDIR /app

# Install requirements
COPY pyproject.toml .
# COPY uv.lock .

RUN uv venv --system-site-packages
RUN uv run uv sync

# copy application files
COPY connected-systems-api connected-systems-api
COPY hypercorn.conf.py .

CMD ["uv", "run", "hypercorn", "-c", "hypercorn.conf.py", "connected-systems-api/app:APP"]