#!/bin/bash

set -eo pipefail

echo "Using '$DJANGO_ENV' environment"

make UV_RUN= migrate
make UV_RUN= collectstatic

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
