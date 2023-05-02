from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestViews(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_login_view_as_anon(self):
        path = reverse("authenticate:login")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

    def test_logout_view_as_anon(self):
        path = reverse("authenticate:logout")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_login_view_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        path = reverse("authenticate:login")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertIs(logged_in, True)

    def test_logout_view_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        path = reverse("authenticate:logout")
        response = self.client.get(path)

        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertIs(logged_in, True)
        self.assertIs(user.is_authenticated, False)

    def test_login_post(self):
        path = reverse("authenticate:login")
        response = self.client.post(path, {
            "username": self.username,
            "password": self.password,
        })

        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertIs(user.is_authenticated, True)
