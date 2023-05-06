from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.contrib import auth
from ao3_web_reader_django.apps.works import forms, models


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestForms(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        self.user = auth.get_user(self.client)

    def test_create_tag_valid_data(self):
        form = forms.AddTagForm(data={
            "tag_name": "test_tag"
        })

        form.user = self.user

        self.assertTrue(form.is_valid())

    def test_create_tag_empty_data(self):
        form = forms.AddTagForm(data={
            "tag_name": ""
        })

        form.user = self.user

        self.assertFalse(form.is_valid())

    def test_create_tag_invalid_data(self):
        models.Tag.objects.create(name="test_tag", owner_id=1)

        form = forms.AddTagForm(data={
            "tag_name": "test_tag"
        })

        form.user = self.user

        self.assertFalse(form.is_valid())
