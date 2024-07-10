from django.conf import settings
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")


class Config:
    enable_utc = True
    timezone = "Europe/Kiev"
    task_serializer = "json"
    result_serializer = "json"
    event_serializer = "json"
    accept_content = ["json"]
    broker_connection_retry_on_startup = (True,)
    broker_connection_max_retries = (5,)
    imports = ("djangoblog.tasks",)
    result_backend = settings.CELERY_RESULT_BACKEND
    broker_url = settings.CELERY_BROKER_URL
    task_always_eager = settings.CELERY_TASK_ALWAYS_EAGER
    task_eager_propagates = settings.CELERY_TASK_EAGER_PROPAGATES
