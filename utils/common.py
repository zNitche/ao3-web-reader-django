from django.http import FileResponse


def send_file(file_path, attachment_name):
    response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=attachment_name)

    return response
