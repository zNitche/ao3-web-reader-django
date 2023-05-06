from django.urls import path
from ao3_web_reader_django.apps.core import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("page/<int:page_id>", views.home, name="home"),
]
