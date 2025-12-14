import os
from django.core.files.base import ContentFile
from django.conf import settings
from .models import GeneratedFile


def extract_text_and_delete(uploaded_file):

    text = uploaded_file.read().decode("utf-8")


    file_path = uploaded_file.temporary_file_path() if hasattr(uploaded_file, 'temporary_file_path') else None

    if file_path and os.path.exists(file_path):

    return text


def create_file_from_text(title: str, text: str, file_type: str):

    file_obj = GeneratedFile.objects.create(
        title=title,
        file_type=file_type
    )

    content = ContentFile(text.encode("utf-8"))

    filename = f"{title}.txt"
    file_obj.file.save(filename, content)

    return file_obj
