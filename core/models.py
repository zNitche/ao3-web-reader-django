from django.db import models
from consts import UpdateMessagesConsts
from django.contrib.auth import get_user_model
from datetime import datetime


class Tag(models.Model):
    name = models.TextField(unique=False, null=False)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Work(models.Model):
    work_id = models.TextField(unique=False, null=False)
    name = models.CharField(max_length=200, unique=False, null=False)
    description = models.TextField(unique=False, null=True)

    date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)
    last_updated = models.DateTimeField(unique=False, null=True, default=datetime.utcnow)

    was_removed = models.BooleanField(unique=False, default=False)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="works")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="works")

    # def get_not_removed_chapters(self):
    #     return [chapter for chapter in self.chapters if not chapter.was_removed]
    #
    # def get_removed_chapters(self):
    #     return [chapter for chapter in self.chapters if chapter.was_removed]
    #
    # def get_completed_chapters(self):
    #     return [chapter for chapter in self.chapters if chapter.completed]
    #
    # def all_chapters_completed(self):
    #     chapters_completion = [chapter.completed for chapter in self.chapters]
    #
    #     return all(chapters_completion)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    chapter_id = models.TextField(unique=False, null=False)
    order_id = models.IntegerField(unique=False, null=True)

    title = models.CharField(max_length=200, unique=False, null=False)
    date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    text = models.TextField(unique=False, null=False)

    was_removed = models.BooleanField(unique=False, null=False, default=False)
    completed = models.BooleanField(unique=False, null=True, default=False)

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="chapters")

    # def get_formatted_text(self):
    #     return self.text.split("\n")
    #
    # def get_next_chapter(self):
    #     prev_chapter = Chapter.query.filter_by(work_id=self.work_id, order_id=self.order_id + 1).first()
    #
    #     return prev_chapter
    #
    # def get_prev_chapter(self):
    #     next_chapter = Chapter.query.filter_by(work_id=self.work_id, order_id=self.order_id - 1).first()
    #
    #     return next_chapter

    def __str__(self):
        return self.title


class UpdateMessage(models.Model):
    chapter_name = models.TextField(unique=False, null=True)
    type = models.TextField(unique=False, null=False, default=UpdateMessagesConsts.MESSAGE_ADDED_TYPE)
    date = models.DateTimeField(unique=False, null=False, default=datetime.utcnow)

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="update_messages")

    def get_message_by_type(self):
        message = None

        if self.type == UpdateMessagesConsts.MESSAGE_ADDED_TYPE:
            message = f"Added '{ self.chapter_name }' to"

        elif self.type == UpdateMessagesConsts.MESSAGE_REMOVED_TYPE:
            message = f"Removed '{self.chapter_name}' from"

        return message
