#!/bin/bash

set -eo pipefail

echo "Using '$DJANGO_ENV' environment"

make migrate
make collectstatic

# Create superuser
make create-superuser
# Generate posts
make create-posts

echo "App is running on PORT: $PORT"
if [ "$DJANGO_ENV" = "production" ]; then
    make prod
else
    make dev
fi
