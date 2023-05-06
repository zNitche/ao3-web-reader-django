from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from apps.works import models


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    })
class TestModels(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "12345678"

        self.client = Client()

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_chapter_get_next_chapter(self):
        models.Tag.objects.create(name="test_tag", owner_id=1)
        models.Work.objects.create(work_id="12345", name="test_work", owner_id=1, tag_id=1)

        first_chapter = models.Chapter.objects.create(
            chapter_id="123", order_id=0, title="t1", text="text1", work_id=1)

        second_chapter = models.Chapter.objects.create(
            chapter_id="124", order_id=1, title="t2", text="text2", work_id=1)

        self.assertIsNot(first_chapter.get_next_chapter(), None)
        self.assertEqual(second_chapter.chapter_id, first_chapter.get_next_chapter().chapter_id)

    def test_chapter_get_prev_chapter(self):
        models.Tag.objects.create(name="test_tag", owner_id=1)
        models.Work.objects.create(work_id="12345", name="test_work", owner_id=1, tag_id=1)

        first_chapter = models.Chapter.objects.create(
            chapter_id="123", order_id=0, title="t1", text="text1", work_id=1)

        second_chapter = models.Chapter.objects.create(
            chapter_id="124", order_id=1, title="t2", text="text2", work_id=1)

        self.assertIsNot(second_chapter.get_prev_chapter(), None)
        self.assertEqual(first_chapter.chapter_id, second_chapter.get_prev_chapter().chapter_id)
