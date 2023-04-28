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

    path("<int:work_id>/remove", views.remove_works, name="remove_work"),
    path("<int:work_id>/download", views.download_work, name="download_work"),
    path("<int:work_id>/mark_chapters_as_incomplete", views.mark_chapters_as_incomplete,
         name="mark_chapters_as_incomplete"),
    path("<int:work_id>/mark_chapters_as_complete", views.mark_chapters_as_complete,
         name="mark_chapters_as_complete"),

    path("<int:work_id>/chapters", views.chapters, name="chapters"),
]
