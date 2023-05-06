from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ao3_web_reader_django.apps.works import forms, models
from ao3_web_reader_django.apps.core.consts import MessagesConsts
from ao3_web_reader_django.utils import files_utils, common
import tempfile
import os


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
    tag = get_object_or_404(models.Tag, id=tag_id, owner=request.user)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)

        for work in tag.works.all():
            work_name = work.name.replace("/", "-")

            work_path = os.path.join(tmp_dir_path, work_name)

            os.mkdir(work_path)

            files_utils.write_work_to_files(work, work_path)

        archive_name = f"{tag.name}.zip"
        archive_path = os.path.join(tmp_dir_path, archive_name)

        files_utils.zip_files(archive_path, tmp_dir_path, (".zip",))

        return common.send_file(archive_path, archive_name)
