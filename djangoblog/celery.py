import logging
from time import time
from typing import Any

from celery import Celery
from celery.signals import task_postrun, task_prerun, worker_init

from djangoblog.celeryconfig import CeleryConfig

logger = logging.getLogger(__name__)


app = Celery("djangoblog")
app.config_from_object(CeleryConfig)

# Load task modules from all registered Django apps
app.autodiscover_tasks()


@worker_init.connect
def init_pyroscope_for_celery(sender: Any, **kwargs: Any) -> None:
    """Initialize Pyroscope profiling for Celery workers."""
    from djangoblog.metrics.pyroscope import init_pyroscope

    worker_name = sender.hostname.split("@")[0] if sender.hostname else "unknown"
    app_name = f"django-blog-celery-{worker_name}"
    init_pyroscope(app_name=app_name)


# Measure celery task execution time
# Ref: https://stackoverflow.com/questions/19481470/measuring-celery-task-execution-time
d: dict[str, Any] = {}


@task_prerun.connect
def task_prerun_handler(
    signal: Any,
    sender: Any,
    task_id: str,
    task: Any,
    args: Any,
    kwargs: Any,
    **extras: Any,
) -> None:
    d[task_id] = time()


@task_postrun.connect
def task_postrun_handler(
    signal: Any,
    sender: Any,
    task_id: str,
    task: Any,
    args: Any,
    kwargs: Any,
    retval: Any,
    **extras: Any,
) -> None:
    try:
        cost = time() - d.pop(task_id)
        payload_size = len(str(retval).encode("utf-8"))
    except KeyError:
        cost = -1

    logger.info(
        f"Task {task.__name__} took {cost}, payload size: {payload_size} bytes",
    )
