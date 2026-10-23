# Build stage: full image has the compilers/libpq headers psycopg2 needs
FROM python:3.11 AS builder
WORKDIR /usr/src/app

RUN pip install poetry==2.1.3

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Runtime stage: slim image avoids hundreds of unused dev packages and their CVEs
FROM python:3.11-slim
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# copy project
COPY . /usr/src/app/
