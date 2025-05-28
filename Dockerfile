FROM python:3.11
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==2.1.3

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# copy project
COPY . /usr/src/app/

