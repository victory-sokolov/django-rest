ARG DEFAULT_PYTHON_VERSION=3.10.14
ARG POETRY_VERSION="1.8.3"

FROM --platform=linux/amd64 python:3.10.14-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    TZ=Etc/GMT-3

RUN set -eux; \
    apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


# Set working directory
WORKDIR /app
ENV DEV_DEPS=0

COPY ./poetry.lock ./pyproject.toml ./

# Check if DEV_DEPS=1 is set, if true, install both main and dev dependencies
# Otherwise, install only main dependencies
RUN if [ "$DEV_DEPS" = "1" ]; then \
    poetry install --no-root; \
    else \
    poetry install --no-root --only main; \
    fi

# Install npm packages
COPY ./package.json ./package-lock.json ./
RUN npm install

# Copy project app
COPY . .

ENV PORT=80
EXPOSE 80

RUN chmod +x ./runserver.sh
CMD ["./runserver.sh"]
