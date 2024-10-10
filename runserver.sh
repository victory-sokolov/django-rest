#!/bin/bash

set -e

echo "Using $DJANGO_ENV environment"

DJANGO_ENV=$DJANGO_ENV python manage.py collectstatic --noinput -i silk/*
DJANGO_ENV=$DJANGO_ENV python manage.py compress --force
DJANGO_ENV=$DJANGO_ENV python manage.py migrate

if [ "$DJANGO_ENV" = "production" ]; then
    DJANGO_ENV=$DJANGO_ENV gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"
else
    # Create superuser
    DJANGO_ENV=$DJANGO_ENV python manage.py create_superuser --user=admin --password=superPassword12 --email=admin@gmail.com
    # Generate posts
    DJANGO_ENV=$DJANGO_ENV python manage.py create_posts --count 100
    DJANGO_ENV=$DJANGO_ENV python manage.py runserver 0.0.0.0:"${PORT:-80}"
fi
