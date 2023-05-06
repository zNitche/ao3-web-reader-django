from django.urls import path
from apps.works.views import works_views, tags_views


app_name = "works"


urlpatterns = [
    path("tags/", tags_views.tags, name="tags"),
    path("tags/add/", tags_views.add_tag, name="add_tag"),
    path("tags/<int:tag_id>/remove/", tags_views.remove_tag, name="remove_tag"),
    path("tags/<int:tag_id>/download/", tags_views.download_tag, name="download_tag"),

    path("add/", works_views.add_work, name="add_work"),

    path("<str:tag_name>/", works_views.works, name="works"),
    path("<str:tag_name>/<int:page_id>/", works_views.works, name="works"),
    path("<str:tag_name>/removed", works_views.removed_works, name="removed_works"),
    path("<str:tag_name>/removed/<int:page_id>/", works_views.removed_works, name="removed_works"),

    path("<str:work_id>/remove/", works_views.remove_work, name="remove_work"),
    path("<str:work_id>/download/", works_views.download_work, name="download_work"),
    path("<str:work_id>/mark_chapters_as_incomplete/", works_views.mark_chapters_as_incomplete,
         name="mark_chapters_as_incomplete"),
    path("<str:work_id>/mark_chapters_as_completed/", works_views.mark_chapters_as_completed,
         name="mark_chapters_as_completed"),
    path("<str:work_id>/chapters/<str:chapter_id>/toggle_completed_state/", works_views.chapter_toggle_completed_state,
         name="chapter_toggle_completed_state"),

    path("<str:work_id>/chapters/", works_views.chapters, name="chapters"),
    path("<str:work_id>/chapters/<str:chapter_id>/", works_views.chapter, name="chapter"),
]
