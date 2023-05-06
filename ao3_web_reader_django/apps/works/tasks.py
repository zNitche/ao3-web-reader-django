from ao3_web_reader_django.celery import app
from ao3_web_reader_django.apps.works.task.scraper_process import ScraperProcess
from ao3_web_reader_django.apps.works.task.works_updater_process import WorksUpdaterProcess


ScraperProcess = app.register_task(ScraperProcess())
WorksUpdaterProcess = app.register_task(WorksUpdaterProcess())
