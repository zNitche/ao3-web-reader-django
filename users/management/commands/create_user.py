from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "create user"

    def handle(self, *args, **options):
        username = input("username: ")
        user = get_user_model().objects.filter(username=username).first()

        if not user:
            password = input("password: ")

            user_model = get_user_model().objects.create_user(username=username, password=password)
            user_model.save()

            self.stdout.write(self.style.SUCCESS(f"{user_model.username} created"))

        else:
            self.stdout.write(self.style.ERROR("user exists"))
