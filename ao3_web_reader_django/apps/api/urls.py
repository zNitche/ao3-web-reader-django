from django.urls import path
from ao3_web_reader_django.apps.api import views


app_name = "api"


urlpatterns = [
    path("sync_status/", views.sync_status, name="sync_status"),
    path("running_scraping_processes/", views.running_scraping_processes, name="running_scraping_processes"),
]
