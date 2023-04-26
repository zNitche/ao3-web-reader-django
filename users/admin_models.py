from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("username", "is_staff", "is_active",)
    list_filter = ("username", "is_staff", "is_active",)

    fieldsets = (
        ("Details", {
            "fields": ("username", "password", "auth_fa_token", "date_joined")
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )

    search_fields = ("username",)
    ordering = ("username",)
    readonly_fields = ("date_joined", "auth_fa_token")
