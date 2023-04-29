from ao3_web_reader_django.celery import app
from works.task.scraper_process import ScraperProcess


ScraperProcess = app.register_task(ScraperProcess())
