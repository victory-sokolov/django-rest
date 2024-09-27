#!/usr/bin/env sh

echo "Using $DJANGO_ENV environment"

DJANGO_ENV=$DJANGO_ENV python manage.py collectstatic --noinput -i silk/*
DJANGO_ENV=$DJANGO_ENV python manage.py compress --force
DJANGO_ENV=$DJANGO_ENV python manage.py migrate
DJANGO_ENV=$DJANGO_ENV gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"
