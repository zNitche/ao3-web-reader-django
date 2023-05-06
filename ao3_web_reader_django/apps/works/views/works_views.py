from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from ao3_web_reader_django.apps.works import tasks
from ao3_web_reader_django.apps.works import forms, models
from ao3_web_reader_django.apps.core.consts import PaginationConsts, MessagesConsts
from ao3_web_reader_django.utils import files_utils, common, tasks_utils
import tempfile
import os


@login_required
@require_http_methods(["GET"])
def works(request, tag_name, page_id=1):
    tag = get_object_or_404(models.Tag, name=tag_name, owner=request.user)

    search_work_name = request.GET.get("search", "")

    works = request.user.works.filter(was_removed=False, tag_id=tag.id,
                                      name__contains=search_work_name).order_by("-last_updated").all()

    works_paginator = Paginator(works, PaginationConsts.WORKS_PER_PAGE)
    works_per_page = works_paginator.get_page(page_id)

    return render(request, "works.html", {"works_paginator": works_paginator,
                                          "works_items": works_per_page,
                                          "tag": tag})


@login_required
@require_http_methods(["GET"])
def removed_works(request, tag_name, page_id=1):
    tag = get_object_or_404(models.Tag, name=tag_name, owner=request.user)
    works = request.user.works.filter(was_removed=True, tag_id=tag.id).order_by("-last_updated").all()

    works_paginator = Paginator(works, PaginationConsts.WORKS_PER_PAGE)
    works_per_page = works_paginator.get_page(page_id)

    return render(request, "works.html", {"works_paginator": works_paginator,
                                          "works_items": works_per_page,
                                          "tag": tag})


@login_required
@require_http_methods(["POST"])
def remove_work(request, work_id):
    page_id = request.GET.get("page_id", 1)

    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)
    work.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.WORK_REMOVED)

    return redirect("works:works", tag_name=work.tag.name, page_id=page_id)


@login_required
@require_http_methods(["GET", "POST"])
def add_work(request):
    form = forms.AddWorkForm(data=request.POST or None)

    user_tags = [(tag.name, tag.name) for tag in request.user.tags.all()]
    form.fields["tag_name"].choices = user_tags

    if request.method == "POST":
        form.user = request.user

        if form.is_valid():
            work_id = request.POST["work_id"]
            tag_name = request.POST["tag_name"]

            task_data = tasks_utils.get_task_data_for_user_and_work(request.user.id, "ScraperProcess", work_id)

            if task_data:
                messages.add_message(request, messages.ERROR,
                                     MessagesConsts.SCRAPING_PROCESS_FOR_WORK_ID_RUNNING.format(work_id=work_id))

            else:
                tasks.ScraperProcess.apply_async((request.user.id, tag_name, work_id))
                messages.add_message(request, messages.SUCCESS, MessagesConsts.SCRAPING_PROCESS_STARTED)

            return redirect("works:add_work")

    return render(request, "add_work.html", {"form": form})


@login_required
@require_http_methods(["GET"])
def download_work(request, work_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)
        files_utils.write_work_to_files(work, tmp_dir_path)

        archive_name = f"{work.name.replace(' ', '_')}.zip"
        archive_path = os.path.join(tmp_dir_path, archive_name)

        files_utils.zip_files(archive_path, tmp_dir_path, (".zip",))

        return common.send_file(archive_path, archive_name)


@login_required
@require_http_methods(["POST"])
def mark_chapters_as_incomplete(request, work_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)
    page_id = request.GET.get("page_id", 1)

    for chapter in work.chapters.all():
        chapter.completed = False
        chapter.save()

    return redirect("works:works", tag_name=work.tag.name, page_id=page_id)


@login_required
@require_http_methods(["POST"])
def mark_chapters_as_completed(request, work_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)
    page_id = request.GET.get("page_id", 1)

    for chapter in work.chapters.all():
        chapter.completed = True
        chapter.save()

    return redirect("works:works", tag_name=work.tag.name, page_id=page_id)


@login_required
@require_http_methods(["GET"])
def chapters(request, work_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)

    available_chapters = work.get_not_removed_chapters()
    removed_chapters = work.get_removed_chapters()

    available_chapters.sort(key=lambda elem: elem.order_id)

    return render(request, "chapters.html", {
        "work": work,
        "available_chapters": available_chapters,
        "removed_chapters": removed_chapters,
    })


@login_required
@require_http_methods(["GET"])
def chapter(request, work_id, chapter_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)
    work_chapter = get_object_or_404(models.Chapter, work_id=work.id, chapter_id=chapter_id)

    return render(request, "chapter.html", {"chapter": work_chapter})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def chapter_toggle_completed_state(request, work_id, chapter_id):
    work = get_object_or_404(models.Work, work_id=work_id, owner=request.user)
    work_chapter = get_object_or_404(models.Chapter, work_id=work.id, chapter_id=chapter_id)

    work_chapter.completed = False if work_chapter.completed else True
    work_chapter.save()

    return JsonResponse(data={}, status=200)
