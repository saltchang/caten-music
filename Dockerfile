FROM python:3.14
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

RUN pip install uv

COPY pyproject.toml uv.lock /usr/src/app/

RUN uv sync --frozen --no-dev

# copy project
COPY . /usr/src/app/
