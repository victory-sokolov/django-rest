import os

from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")


class CeleryConfig:
    enable_utc = True
    timezone = "Europe/Kiev"
    task_serializer = "msgpack"
    result_serializer = "msgpack"
    event_serializer = "msgpack"
    accept_content = ["json", "msgpack"]
    broker_connection_retry_on_startup = True
    # Compress task payloads and results to reduce size in transport/result backend
    task_compression = "gzip"
    result_compression = "gzip"
    task_compression_level = 6
    result_persistent = False
    hijack_root_logger = False
    broker_connection_max_retries = 5
    worker_concurrency = 8
    imports = ("djangoblog.tasks",)
    task_default_queue = "blog"
    result_backend = settings.CELERY_RESULT_BACKEND
    broker_url = settings.CELERY_BROKER_URL
    task_always_eager = settings.CELERY_TASK_ALWAYS_EAGER
    task_eager_propagates = settings.CELERY_TASK_EAGER_PROPAGATES
    task_ack_late = True
    # Send task-related events so that tasks can be monitored using tools like flower
    worker_send_task_events = True
    # The SENT event indicates when a task is sent
    task_send_sent_event = True
    worker_max_tasks_per_child = 100
    worker_max_memory_per_child = 350000  # 350 MB
    result_expires = 600  # 10 minutes
