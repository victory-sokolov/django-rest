import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")


class Config:
    enable_utc = True
    timezone = "Europe/Kiev"
    result_backend = "rpc://"
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    imports = ("djangoblog.tasks",)
