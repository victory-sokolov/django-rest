#!/bin/bash

set -eo pipefail

echo "Using '$DJANGO_ENV' environment"

make migrate
make collectstatic

# Create superuser
make create-superuser
# Generate posts
make create-posts

wait-for-it \
  --host="$DB_HOST" \
  --port="$PGPORT" \
  --timeout=90 \
  --strict

echo "Postgres ${DB_HOST}:${PGPORT} is up"

echo "App is running on PORT: $PORT"
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Running with prod config"
    make prod
else
    echo "Running with dev config"
    make dev
fi
