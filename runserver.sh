#!/usr/bin/env sh

DJANGO_ENV=production python manage.py collectstatic \
    --noinput \
    -i tagify \
    -i django_extensions \
    -i rest_framework
# DJANGO_ENV=production python manage.py compress --force
DJANGO_ENV=production python manage.py compression
DJANGO_ENV=production python manage.py migrate
DJANGO_ENV=production gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"
