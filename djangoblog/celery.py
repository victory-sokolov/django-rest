import logging
from time import time
from typing import Any

from celery import Celery
from celery.signals import task_postrun, task_prerun

from djangoblog.celeryconfig import CeleryConfig

logger = logging.getLogger(__name__)


app = Celery("djangoblog")
app.config_from_object(CeleryConfig)

# Load task modules from all registered Django apps
app.autodiscover_tasks()

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
    **extras: Any,
) -> None:
    try:
        cost = time() - d.pop(task_id)
    except KeyError:
        cost = -1

    logger.info(f"Task {task.__name__} took {cost}")
