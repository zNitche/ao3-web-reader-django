from django.core.exceptions import ValidationError


class PasswordLengthValidator:
    def __init__(self):
        self.min_length = 8
        self.max_length = 32

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(f"Password must contain at least {self.min_length} characters.")

        elif len(password) > self.max_length:
            raise ValidationError(f"Password cant have more than {self.max_length} characters.")

    def get_help_text(self):
        return f"Password must contain at least {self.min_length} and no more than {self.max_length} characters"
