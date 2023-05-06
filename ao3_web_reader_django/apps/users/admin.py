from django.contrib import admin
from ao3_web_reader_django.apps.users.models import User
from ao3_web_reader_django.apps.users.admin_models import CustomUserAdmin


admin.site.register(User, CustomUserAdmin)
