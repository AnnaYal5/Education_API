from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import get_file_content_service, FileServiceError


@api_view(['GET'])
def get_file_content(request, file_id):
    try:
        title, content = get_file_content_service(file_id)

        return Response({
            'file_id': file_id,
            'title': title,
            'content': content
        }, status=status.HTTP_200_OK)

    except FileServiceError as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception:
        return Response(
            {"detail": "Невідома внутрішня помилка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )