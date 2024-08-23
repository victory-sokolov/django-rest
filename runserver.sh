#!/usr/bin/env sh

DJANGO_ENV=production python manage.py collectstatic --noinput
DJANGO_ENV=production python manage.py migrate
DJANGO_ENV=production gunicorn djangoblog.wsgi:application --config gunicorn.py --bind 0.0.0.0:"${PORT:-80}"
