from ao3_web_reader_django.celery import app
from django.core.cache import cache
import logging


logger = logging.getLogger("celery_logger")


@app.task(bind=True)
def debug_task(self):
    logger.debug("TEST CELERY LOG")

    cache.set("test_task", "hello, world!", 30)
    print(f'Request: {self.request}')
