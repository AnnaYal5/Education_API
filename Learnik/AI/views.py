from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from asgiref.sync import async_to_sync

from .services import AICommunicator

from .pydantic_models.ai_models import (
    AICreateConspectModel,
    AICreateTestModel,
    AICreateBookModel
)

from .serializers import (
    AICreateConspectSerializer,
    AIResponseSerializer,
    AICreateTestSerializer,
    AICreateBookSerializer
)

# ============= Генерація конспекту =============
@extend_schema(
    request=AICreateConspectSerializer,
    responses=AIResponseSerializer,
    description="Генерація конспекту за допомогою AI"
)
@permission_classes([AllowAny])
@api_view(['POST'])
def create_conspect(request):
    serializer = AICreateConspectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    ai_request = AICreateConspectModel(**data)
    ai_communicator = AICommunicator()

    try:
        conspect_html = async_to_sync(ai_communicator.generate_conspect)(
            theme=ai_request.topic,
            count_words=ai_request.words_count,
            language=ai_request.language,
            complexity=ai_request.complexity,
            style=ai_request.style,
            font=ai_request.font,
            size_font=ai_request.font_size
        )

        response_serializer = AIResponseSerializer({"text": conspect_html})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {"detail": "Невідома внутрішня помилка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ============= Генерація тесту =============
@extend_schema(
    request=AICreateTestSerializer,
    responses=AIResponseSerializer,
    description="Генерація тесту за допомогою AI"
)
@permission_classes([AllowAny])
@api_view(['POST'])
def create_test(request):
    serializer = AICreateTestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    ai_request = AICreateTestModel(**data)
    ai_communicator = AICommunicator()

    try:
        test_html = async_to_sync(ai_communicator.generate_test)(
            theme=ai_request.topic,
            count_questions=ai_request.questions_count,
            difficulty=ai_request.difficulty,
            language=ai_request.language,
            font=ai_request.font,
            font_size=ai_request.font_size
        )

        response_serializer = AIResponseSerializer({"text": test_html})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Невідома внутрішня помилка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
# ============= Аналіз книги =============
@extend_schema(
    request=AICreateBookSerializer,
    responses=AIResponseSerializer,
    description="Аналіз книги за допомогою AI"
)

@permission_classes([AllowAny])
@api_view(['POST'])
def analyze_book(request):
    serializer = AICreateBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    ai_request = AICreateBookModel(**data)
    ai_communicator = AICommunicator()

    try:
        analysis_html = async_to_sync(ai_communicator.generate_book)(
            text=ai_request.text,
            language=ai_request.language,
            style=ai_request.style,
            font=ai_request.font,
            size_font=ai_request.font_size
        )

        response_serializer = AIResponseSerializer({"text": analysis_html})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Невідома внутрішня помилка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )