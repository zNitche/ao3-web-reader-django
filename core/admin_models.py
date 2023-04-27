from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class WorkAdmin(admin.ModelAdmin):
    list_display = ("work_id", "name", "description", "date", "last_updated", "was_removed")
    search_fields = ("work_id", "name")

    readonly_fields = ["date"]


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("chapter_id", "order_id", "title", "date", "text", "was_removed", "completed")
    search_fields = ("chapter_id", "title")

    readonly_fields = ["date"]


class UpdateMessageAdmin(admin.ModelAdmin):
    list_display = ("chapter_name", "type", "date")
    search_fields = ("uchapter_namer", "type")

    readonly_fields = ["date"]
