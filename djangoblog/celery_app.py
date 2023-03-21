import logging
from time import time
from celery.signals import task_prerun, task_postrun
from celery import Celery

from djangoblog.celeryconfig import Config

logger = logging.getLogger(__name__)

app = Celery("tasks")
app.config_from_object(Config)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Measure celery task execution time
# Ref: https://stackoverflow.com/questions/19481470/measuring-celery-task-execution-time
d = {}

@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    d[task_id] = time()


@task_postrun.connect
def task_postrun_handler(
    signal, sender, task_id, task, args, kwargs, retval, state, **extras
):
    try:
        cost = time() - d.pop(task_id)
    except KeyError:
        cost = -1

    logger.info(f"Task {task.__name__} took {cost}")
