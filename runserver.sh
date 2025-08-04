#!/bin/bash

set -eo pipefail

echo "Using '$DJANGO_ENV' environment"

make UV_RUN= migrate
make UV_RUN= collectstatic

# Create superuser
make UV_RUN= create-superuser
# Generate posts
make UV_RUN= create-posts

wait-for-it \
  --host="$DB_HOST" \
  --port="$PGPORT" \
  --timeout=90 \
  --strict

echo "Postgres ${DB_HOST}:${PGPORT} is up"

echo "App is running on PORT: $PORT"
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Running with $DJANGO_ENV config"
    make UV_RUN= prod
else
    echo "Running with dev config"
    make dev
fi
