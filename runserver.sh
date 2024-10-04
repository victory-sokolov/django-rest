#!/bin/bash

set -e

echo "Using $DJANGO_ENV environment"

DJANGO_ENV=$DJANGO_ENV uv run python manage.py check --settings=djangoblog.settings --deploy
DJANGO_ENV=$DJANGO_ENV uv run python manage.py collectstatic --noinput -i silk/*
DJANGO_ENV=$DJANGO_ENV uv run python manage.py compress --force
DJANGO_ENV=$DJANGO_ENV uv run python manage.py migrate

if [ "$DJANGO_ENV" = "production" ]; then
    DJANGO_ENV=$DJANGO_ENV uv run gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"
else
    DJANGO_ENV=$DJANGO_ENV uv run python manage.py runserver
fi
