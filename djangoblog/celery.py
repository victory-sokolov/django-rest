import os

from celery import Celery
from djangoblog.celeryconfig import Config

app = Celery("tasks")
app.config_from_object(Config)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
