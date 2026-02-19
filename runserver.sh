#!/bin/bash

set -eo pipefail

echo "Using '$DJANGO_ENV' environment"

# Only run migrations if there are pending ones
if DJANGO_ENV="$DJANGO_ENV" python manage.py migrate --plan 2>/dev/null | grep -q '\[ \]'; then
    echo "Pending migrations found, running migrate..."
    make UV_RUN= migrate
else
    echo "No pending migrations, skipping..."
fi

# Static files are collected at build time in Dockerfile

# Create superuser
make UV_RUN= create-superuser
# Generate posts
make UV_RUN= create-posts

echo "App is running on PORT: $PORT"
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Running with $DJANGO_ENV config"
    make UV_RUN= prod
else
    echo "Running with dev config"
    make dev
fi
