from django.test import TestCase, Client, override_settings
from django.shortcuts import resolve_url
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
from apps.works import models


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

    def test_create_tag_as_non_auth(self):
        path = reverse("works:add_tag")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)

    def test_create_tag_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        path = reverse("works:add_tag")
        response = self.client.post(path, {
            "tag_name": "test_tag",
        })

        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertIs(user.is_authenticated, True)
        self.assertIs(logged_in, True)

        tag = models.Tag.objects.filter(name="test_tag").first()
        self.assertIsNot(tag, None)

    def test_remove_tag_as_non_auth(self):
        path = resolve_url("works:remove_tag", tag_id=0)
        response = self.client.post(path)

        self.assertEqual(response.status_code, 302)

    def test_remove_tag_as_auth(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        user = auth.get_user(self.client)

        self.assertIs(user.is_authenticated, True)
        self.assertIs(logged_in, True)

        test_tag = models.Tag.objects.create(name="test_tag", owner_id=user.id)

        path = resolve_url("works:remove_tag", tag_id=test_tag.id)
        response = self.client.post(path)

        self.assertEqual(response.status_code, 302)

        tag = models.Tag.objects.filter(name=test_tag.name).first()
        self.assertIs(tag, None)
