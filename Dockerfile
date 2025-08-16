ARG DEFAULT_PYTHON_VERSION=3.12.11

FROM --platform=$BUILDPLATFORM python:3.13.7-bookworm@sha256:d13a8bc66d12516750ccfc46be1334401bea0bf6e4c92ca7f77e099a468891c9 AS base

ARG DEV_DEPS=false

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    TZ=Europe/Riga \
    LANG=C.UTF-8

RUN set -eux; \
    apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    iputils-ping \
    build-essential \
    libpq-dev \
    gettext \
    wait-for-it \
    vim; \
    if [ "$DEV_DEPS" = "true" ]; then \
    apt-get install --no-install-recommends -y make; \
    fi; \
    apt-get clean && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*


FROM node:22-alpine3.19 AS frontend

WORKDIR /frontend

# Install npm packages
COPY ./package.json ./package-lock.json ./
RUN npm install


FROM base AS python_builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

RUN pip install -U uv
COPY uv.lock pyproject.toml ./


# Check if DEV_DEPS=true is set, if true, install both main and dev dependencies
# Otherwise, install only main dependencies
RUN --mount=type=cache,target=/app/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    if [ "$DEV_DEPS" = "true" ]; then \
    echo "Installing all dependencies including dev"; \
    python -m uv sync --no-install-project --frozen; \
    else \
    echo "Installing production dependencies"; \
    python -m uv sync --no-install-project --frozen --no-editable --no-dev; \
    fi

FROM python_builder AS production

WORKDIR /app

# Copy build python
COPY --chown=app:app --from=python_builder /app /app
COPY --chown=app:app --from=frontend /frontend/node_modules /app/node_modules
COPY --chown=app . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=80
EXPOSE 80

# Mount secret key
RUN --mount=type=secret,id=SECRET_KEY,target=/run/secrets/SECRET_KEY,required=false \
    if [ -f /run/secrets/SECRET_KEY ]; then \
    export SECRET_KEY=$(cat /run/secrets/SECRET_KEY); \
    echo "Secret key loaded successfully"; \
    else \
    echo "No secret key found"; \
    fi && \
    make run-checks

RUN chmod +x ./runserver.sh
CMD ["./runserver.sh"]
