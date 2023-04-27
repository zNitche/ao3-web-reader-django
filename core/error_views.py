from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def not_found(request, exception=None):
    return render(request, "error.html", status=404, context={"error": "not found"})


@require_http_methods(["GET"])
def server_error(request, exception=None):
    return render(request, "error.html", status=500, context={"error": "server error"})


@require_http_methods(["GET"])
def bad_request(request, exception=None):
    return render(request, "error.html", status=400, context={"error": "bad request"})
