import os

from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")


class CeleryConfig:
    enable_utc = True
    timezone = "Europe/Kiev"
    task_serializer = "json"
    result_serializer = "json"
    event_serializer = "json"
    accept_content = ["json"]
    broker_connection_retry_on_startup = (True,)
    hijack_root_logger = False
    broker_connection_max_retries = (5,)
    imports = ("djangoblog.tasks",)
    result_backend = settings.CELERY_RESULT_BACKEND
    broker_url = settings.CELERY_BROKER_URL
    task_always_eager = settings.CELERY_TASK_ALWAYS_EAGER
    task_eager_propagates = settings.CELERY_TASK_EAGER_PROPAGATES
    task_ack_late = True
    worker_max_tasks_per_child = 100
    worker_max_memory_per_child = 200000  # 200 MB
