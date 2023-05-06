from django import forms
from django.core.exceptions import ValidationError
from ao3_web_reader_django.apps.core.consts import MessagesConsts
from ao3_web_reader_django.apps.works import models
from ao3_web_reader_django.utils import works_utils


class AddTagForm(forms.Form):
    tag_name = forms.CharField(label="Tag name", required=True)

    template_name = "components/form.html"

    def clean_tag_name(self):
        data = self.cleaned_data["tag_name"]
        tag = models.Tag.objects.filter(owner=self.user, name=data).first()

        if tag:
            raise ValidationError(MessagesConsts.TAG_ALREADY_ADDED)

        return data


class AddWorkForm(forms.Form):
    work_id = forms.CharField(label="Work ID", required=True)
    tag_name = forms.ChoiceField(label="", required=True)

    template_name = "components/form.html"

    def clean_work_id(self):
        data = self.cleaned_data["work_id"]

        if not works_utils.check_if_work_is_accessible(data):
            raise ValidationError(MessagesConsts.CANT_ACCESS_WORK)

        work = models.Work.objects.filter(owner=self.user, work_id=data).first()

        if work:
            raise ValidationError(MessagesConsts.WORK_ALREADY_ADDED)

        return data

    def clean_tag_name(self):
        data = self.cleaned_data["tag_name"]
        tag = models.Tag.objects.filter(owner=self.user, name=data).first()

        if not tag:
            raise ValidationError(MessagesConsts.TAG_DOESNT_EXIST)

        return data
