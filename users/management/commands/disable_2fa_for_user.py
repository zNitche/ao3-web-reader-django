from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "disable 2fa for user"

    def add_arguments(self, parser):
        parser.add_argument("--username", "-u", type=str, default=None)

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options.get("username")).first()

        if user:
            user.auth_fa_token = None
            user.save()

            self.stdout.write(self.style.SUCCESS(f"2fa disabled for: {user.username}"))

        else:
            self.stdout.write(self.style.ERROR("user doesn't exist"))
