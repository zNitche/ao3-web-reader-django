from django.contrib import admin
from users.models import User
from users.admin_models import CustomUserAdmin


admin.site.register(User, CustomUserAdmin)
