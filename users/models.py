from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
