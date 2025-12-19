import os
from django.conf import settings
from django.http import FileResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import TextStorage

# Читає текст від користувача та видаляє файл
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary',
                    'description': 'Text file to upload'
                }
            }
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': 'Extracted text from file'
                }
            }
        }
    },
    description='Upload a text file and extract its content',
    tags=['Files']
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_file_and_read_text(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    uploaded_file = request.FILES['file']
    temp_path = settings.MEDIA_ROOT / uploaded_file.name

    with open(temp_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    with open(temp_path, 'r', encoding='utf-8') as f:
        text = f.read()

    os.remove(temp_path)

    return Response({"text": text})


# Текст береться з БД та повертається як файл
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='text_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID of the text storage object'
        )
    ],
    responses={
        200: {
            'type': 'string',
            'format': 'binary',
            'description': 'Text file download'
        },
        404: {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'}
            }
        }
    },
    description='Download stored text as a file',
    tags=['Files']
)
@api_view(['GET'])
def download_text_as_file(request, text_id):
    try:
        obj = TextStorage.objects.get(id=text_id)
    except TextStorage.DoesNotExist:
        return Response(
            {"error": "Text not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    content = ContentFile(obj.text.encode('utf-8'))

    response = FileResponse(
        content,
        as_attachment=True,
        filename=f"{obj.title}.txt"
    )

    return response