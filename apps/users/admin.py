from django.contrib import admin
from apps.users.models import User
from apps.users.admin_models import CustomUserAdmin


admin.site.register(User, CustomUserAdmin)
