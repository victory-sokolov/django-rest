import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")


class Config:
    enable_utc = True
    timezone = "Europe/Kiev"
    result_backend = "rpc://"
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    broker_connection_retry_on_startup = (True,)
    broker_connection_max_retries = (5,)
    imports = ("djangoblog.tasks",)
