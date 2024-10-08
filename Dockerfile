ARG DEFAULT_PYTHON_VERSION=3.12.7

FROM --platform=linux/amd64 python:3.12.7-bookworm AS base

ARG DEV_DEPS=false

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # PYTHONHASHSEED=random \
    # PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
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


FROM node:22-alpine3.19 AS frontend

WORKDIR /frontend

# Install npm packages
COPY ./package.json ./package-lock.json ./
RUN npm install


FROM base AS python_builder

RUN pip install uv
COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/app/.cache/uv \
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

FROM python_builder AS production

# Copy build python
COPY --chown=app --from=python_builder /app /app
COPY --chown=app --from=frontend /frontend/node_modules /app/node_modules
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=80
EXPOSE 80

RUN chmod +x ./runserver.sh
CMD ["./runserver.sh"]
