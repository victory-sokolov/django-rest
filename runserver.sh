#!/bin/bash

set -eo pipefail

echo "Using $DJANGO_ENV environment"

make migrate
make collectstatic
DJANGO_ENV=$DJANGO_ENV python manage.py compress --force

# Create superuser
make create-superuser
# Generate posts
DJANGO_ENV=$DJANGO_ENV python manage.py create_posts --count 100

if [ "$DJANGO_ENV" = "production" ]; then
    make prod
else
    make dev
    DJANGO_ENV=$DJANGO_ENV python manage.py runserver 0.0.0.0:"${PORT:-80}"
fi
