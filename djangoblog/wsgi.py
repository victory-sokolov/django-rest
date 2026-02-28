"""
WSGI config for djangoblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")

# Initialize Pyroscope profiling before loading the WSGI application
from djangoblog.metrics.pyroscope import init_pyroscope

init_pyroscope(app_name="django-blog-gunicorn")

application = get_wsgi_application()
