from django.shortcuts import get_object_or_404
from .models import  FileLearning
import os


class FileServiceError(Exception):
    pass


def get_file_content_service(file_id: int) -> tuple[str, str]:
    learning_file = get_object_or_404( FileLearning, id=file_id)
    file_path = learning_file.file.path

    if not os.path.exists(file_path):
        raise FileServiceError("не знайдено на сервері.")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

    except Exception as e:
        raise FileServiceError(f"Сталася помилка при читанні файлу: {e}")

    return learning_file.title, content