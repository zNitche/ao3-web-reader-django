from django.contrib import admin
from ao3_web_reader_django.apps.works import admin_models, models

# Register your models here.
admin.site.register(models.Tag, admin_models.TagAdmin)
admin.site.register(models.Work, admin_models.WorkAdmin)
admin.site.register(models.Chapter, admin_models.ChapterAdmin)
admin.site.register(models.UpdateMessage, admin_models.UpdateMessageAdmin)
