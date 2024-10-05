ARG DEFAULT_PYTHON_VERSION=3.12.7

FROM --platform=linux/amd64 python:3.12.7-bookworm

ARG DEV_DEPS=false

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONHASHSEED=random \
    TZ=Etc/GMT-3

RUN set -eux; \
    apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    vim; \
    if [ "$DEV_DEPS" = "true" ]; then \
    apt-get install --no-install-recommends -y make; \
    fi; \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs


# Set working directory
WORKDIR /app

USER root

RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install uv
COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml

# Check if DEV_DEPS=true is set, if true, install both main and dev dependencies
# Otherwise, install only main dependencies
RUN if [ "$DEV_DEPS" = "true" ]; then \
    echo "Installing all dependencies including dev"; \
    uv sync --no-install-project --extra dev --frozen; \
    else \
    echo "Installing production dependencies"; \
    uv sync --no-install-project --frozen; \
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
