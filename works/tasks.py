from ao3_web_reader_django.celery import app
from works.task.scraper_process import ScraperProcess
from works.task.works_updater_process import WorksUpdaterProcess


ScraperProcess = app.register_task(ScraperProcess())
WorksUpdaterProcess = app.register_task(WorksUpdaterProcess())
