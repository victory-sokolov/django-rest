#!/usr/bin/env sh

# Getting static files for Admin panel hosting!
DJANGO_ENV=production python manage.py collectstatic --noinput
DJANGO_ENV=production python manage.py migrate
DJANGO_ENV=production gunicorn djangoblog.wsgi:application --bind 0.0.0.0:"${PORT}"
