import os
from celery import Celery
from celery.signals import worker_ready
from ao3_web_reader_django.apps.core.consts import TasksDelays


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ao3_web_reader_django.settings")

app = Celery("ao3_web_reader_django")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    app.conf.beat_schedule["WorksUpdaterProcess"] = {
        "task": "ao3_web_reader_django.apps.works.task.works_updater_process.WorksUpdaterProcess",
        "schedule": TasksDelays.WORKS_UPDATER_INTERVAL,
    }


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
         sender.app.send_task("ao3_web_reader_django.apps.works.task.works_updater_process.WorksUpdaterProcess", connection=conn)
