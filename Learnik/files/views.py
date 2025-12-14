import os
from django.conf import settings
from django.http import JsonResponse
from django.http import FileResponse
from django.core.files.base import ContentFile
from .models import TextStorage

#читає текст від користувача та видаляє
def upload_file_and_read_text(request):

    uploaded_file = request.FILES['file']

    temp_path = settings.MEDIA_ROOT / uploaded_file.name

    with open(temp_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    with open(temp_path, 'r', encoding='utf-8') as f:
        text = f.read()

    os.remove(temp_path)

    return JsonResponse({
        "text": text
    })

#текст береться з бд та після створення видаляється файл
def download_text_as_file(request, text_id):

    obj = TextStorage.objects.get(id=text_id)

    content = ContentFile(obj.text.encode('utf-8'))

    response = FileResponse(
        content,
        as_attachment=True,
        filename=f"{obj.title}.txt"
    )

    return response
