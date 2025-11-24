from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import  FileLearning


@api_view(['GET'])
def get_file_content(request, file_id):
    try:
        learning_file = get_object_or_404(FileLearning, id=file_id)

        file_path = learning_file.file.path
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return Response({
            'file_id': file_id,
            'title': learning_file.title,
            'content': content
        }, status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response(
            {"detail": "Файл не знайдено."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"detail": f"Помилка при читанні файлу: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
