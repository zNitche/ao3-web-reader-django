from django.http import HttpResponse


def send_file(file_path, attachment_name, content_type="application/json"):
    response = HttpResponse(open(file_path), content_type=content_type)
    response["Content-Disposition"] = f"attachment; filename={attachment_name}"

    return response
