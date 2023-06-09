from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ao3_web_reader_django.consts import ProcessesConsts
from ao3_web_reader_django.utils import tasks_utils


@login_required
@require_http_methods(["GET"])
def sync_status(request):
    sync_process_cache_keys = tasks_utils.get_tasks_keys_by_type("WorksUpdaterProcess")

    sync_process_cache_key = sync_process_cache_keys[0] if len(sync_process_cache_keys) == 1 else None
    sync_process_data = tasks_utils.get_task_data_by_key(sync_process_cache_key)

    sync_process_running = True if sync_process_data else False
    response = {
        "is_running": sync_process_running,
        "progress": sync_process_data.get(ProcessesConsts.PROGRESS) if sync_process_running else 0,
    }

    return JsonResponse(data=response, status=200)


@login_required
@require_http_methods(["GET"])
def running_scraping_processes(request):
    running_tasks_data = tasks_utils.get_tasks_data_for_user(request.user.id, "ScraperProcess")

    response = {
        "processes_data": running_tasks_data
    }

    return JsonResponse(data=response, status=200)
