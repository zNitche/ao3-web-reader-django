from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from works import models
from works import forms
from consts import PaginationConsts, MessagesConsts


# Tags
@login_required
@require_http_methods(["GET"])
def tags(request):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["GET", "POST"])
def add_tag(request):
    form = forms.AddTagForm(data=request.POST or None)

    if request.method == "POST":
        form.user = request.user

        if form.is_valid():
            tag_name = request.POST["tag_name"]

            tag = models.Tag(name=tag_name, owner=request.user)
            tag.save()

            messages.add_message(request, messages.SUCCESS, MessagesConsts.ADDED_TAG.format(tag_name=tag.name))

    return render(request, "add_tag.html", {"tags": tags, "form": form})


@login_required
@require_http_methods(["POST"])
def remove_tag(request, tag_id):
    tag = get_object_or_404(models.Tag, id=tag_id, owner=request.user)
    tag.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.TAG_REMOVED)

    return redirect("works:tags")


@login_required
@require_http_methods(["GET"])
def download_tag(request, tag_id):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


#Works
@login_required
@require_http_methods(["GET"])
def works(request, tag_name, page_id=1):
    tag = get_object_or_404(models.Tag, name=tag_name, owner=request.user)
    works = request.user.works.filter(was_removed=False, tag_id=tag.id).order_by("-last_updated").all()

    works_paginator = Paginator(works, PaginationConsts.WORKS_PER_PAGE)
    works_per_page = works_paginator.get_page(page_id)

    return render(request, "works.html", {"works_paginator": works_paginator,
                                          "works_items": works_per_page,
                                          "tag": tag})


@login_required
@require_http_methods(["GET"])
def removed_works(request):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["POST"])
def remove_works(request, work_id, tag_name):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["GET"])
def download_work(request, work_id):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["POST"])
def mark_chapters_as_incomplete(request, work_id):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["POST"])
def mark_chapters_as_complete(request, work_id):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})


@login_required
@require_http_methods(["GET"])
def chapters(request, work_id):
    tags = request.user.tags.all()

    return render(request, "tags.html", {"tags": tags})

