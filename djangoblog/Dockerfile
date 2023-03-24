FROM python:3.10.1-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    gunicorn

# Install Poetry
# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.4.1
RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="${PATH}:/root/.local/bin"

# copy entrypoint.sh
# COPY entrypoint.sh .
# RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
# RUN chmod +x /usr/src/app/entrypoint.sh


# Set working directory
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main

# Copy project app
COPY . .
