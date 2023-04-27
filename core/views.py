from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from works import models
from consts import PaginationConsts


@login_required
@require_http_methods(["GET"])
def home(request, page_id=1):
    user_works_ids = [work.id for work in request.user.works.all()]
    update_messages = models.UpdateMessage.objects.filter(work_id__in=user_works_ids).order_by("-date").all()

    messages_pagination = Paginator(update_messages, PaginationConsts.UPDATE_MESSAGES_PER_PAGE)
    messages_page = messages_pagination.get_page(page_id)

    return render(request, "index.html", {"update_messages_page": messages_page,
                                          "update_messages": messages_page.object_list})
