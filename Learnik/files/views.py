from django.http import FileResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import GeneratedFile
from .services import extract_text_and_delete, create_file_from_text
from .serializers import (
    FileUploadSerializer,
    TextGenerationSerializer,
    FileResponseSerializer,
    TextResponseSerializer
)


@extend_schema(
    description='Завантажити файл та виділити текст',
    request=FileUploadSerializer,
    responses={200: TextResponseSerializer}
)
@parser_classes((MultiPartParser, FormParser))
@api_view(['POST'])
def upload_file_and_read_text(request):
    serializer = FileUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    file = serializer.validated_data['file']
    text = extract_text_and_delete(file)
    return Response({'text': text}, status=status.HTTP_200_OK)


@extend_schema(
    description='Завантажити текст як файл',
    responses={200: FileResponseSerializer}
)
@api_view(['GET'])
def download_text_as_file(request, text_id):
    try:
        obj = GeneratedFile.objects.get(id=text_id)
        return FileResponse(
            obj.file.open("rb"),
            as_attachment=True,
            filename=obj.file.name
        )
    except GeneratedFile.DoesNotExist:
        return Response(
            {'error': 'Файл не знайдено'},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(
    description='Генерувати файл з тексту та завантажити',
    request=TextGenerationSerializer,
    responses={201: FileResponseSerializer}
)
@parser_classes((MultiPartParser, FormParser))
@api_view(['POST'])
def generate_file_from_text(request):
    serializer = TextGenerationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    file_obj = create_file_from_text(
        serializer.validated_data['title'],
        serializer.validated_data['text'],
        serializer.validated_data['file_type']
    )
    
    return Response(
        {'file_id': file_obj.id, 'filename': file_obj.file.name},
        status=status.HTTP_201_CREATED
    )