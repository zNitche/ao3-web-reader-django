from django import forms
from django.core.exceptions import ValidationError
from consts import MessagesConsts
from works import models


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

    template_name = "components/form.html"

    def clean_work_id(self):
        data = self.cleaned_data["work_id"]
        work = models.Work.objects.filter(owner=self.user, work_id=data).first()

        if work:
            raise ValidationError(MessagesConsts.WORK_ALREADY_ADDED)

        return data
