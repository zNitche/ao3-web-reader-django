from ao3_web_reader_django.celery import app
from django.core.cache import cache


@app.task(bind=True)
def debug_task(self):
    cache.set("test_task", "hello, world!", 30)
    print(f'Request: {self.request}')
