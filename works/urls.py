from django.urls import path
from works import views


app_name = "works"

urlpatterns = [
    path("tags/", views.tags, name="tags"),
    path("tags/add/", views.add_tag, name="add_tag"),
    path("tags/<int:tag_id>/remove/", views.remove_tag, name="remove_tag"),
    path("tags/<int:tag_id>/download/", views.download_tag, name="download_tag"),

    path("<str:tag_name>/", views.works, name="works"),
    path("<str:tag_name>/<int:page_id>/", views.works, name="works"),
    path("<str:tag_name>/removed", views.removed_works, name="removed_works"),
    path("<str:tag_name>/removed/<int:page_id>/", views.removed_works, name="removed_works"),

    path("<str:work_id>/remove", views.remove_works, name="remove_work"),
    path("<str:work_id>/download", views.download_work, name="download_work"),
    path("<str:work_id>/mark_chapters_as_incomplete", views.mark_chapters_as_incomplete,
         name="mark_chapters_as_incomplete"),
    path("<str:work_id>/mark_chapters_as_complete", views.mark_chapters_as_complete,
         name="mark_chapters_as_complete"),
    path("<str:work_id>/chapters/<str:chapter_id>/toggle_completed_state", views.chapter_toggle_completed_state,
         name="chapter_toggle_completed_state"),

    path("<str:work_id>/chapters", views.chapters, name="chapters"),
    path("<str:work_id>/chapters/<str:chapter_id>", views.chapter, name="chapter"),
]
