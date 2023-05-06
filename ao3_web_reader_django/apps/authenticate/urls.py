from django.urls import path
from ao3_web_reader_django.apps.authenticate import views

app_name = "authenticate"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
