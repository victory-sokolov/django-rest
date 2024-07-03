import os


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
    result_backend = os.environ.get(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379",
    )
    CELERY_BROKER_URL = os.environ.get(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379",
    )
