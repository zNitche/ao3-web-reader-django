from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import pyotp


class Command(BaseCommand):
    help = "enable 2fa for user"

    def add_arguments(self, parser):
        parser.add_argument("--username", "-u", type=str, default=None)

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options.get("username")).first()

        if user:
            if user.auth_fa_token is not None:
                self.stdout.write("2fa token for user exists do you want to override it ? yes/no")
                choice = input("> ").lower()

                if choice == "yes":
                    self.set_2fa_token(user)

                elif choice == "no":
                    self.stdout.write(self.style.SUCCESS(f"user token: {user.auth_fa_token}"))

                else:
                    self.stdout.write(self.style.ERROR("unknown choice"))
            else:
                self.set_2fa_token(user)
        else:
            self.stdout.write(self.style.ERROR("user doesn't exist"))

    def set_2fa_token(self, user):
        token = pyotp.random_base32()
        self.stdout.write(f"token: {token}")
        auth_code = input("auth code > ")

        totp = pyotp.TOTP(token)

        if totp.verify(auth_code):
            user.auth_fa_token = token
            user.save()

            self.stdout.write(self.style.SUCCESS(f"code match, 2fa enabled for {user.username}"))

        else:
            self.stdout.write(self.style.ERROR("code doesnt match"))
