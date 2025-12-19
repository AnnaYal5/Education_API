from django.http import FileResponse
from .models import GeneratedFile


def download_text_as_file(request, text_id):
    obj = GeneratedFile.objects.get(id=text_id)

    return FileResponse(
        obj.file.open("rb"),
        as_attachment=True,
        filename=obj.file.name
    )
