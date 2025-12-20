from django.urls import path
from .views import upload_file_and_read_text, download_text_as_file, generate_file_from_text

urlpatterns = [
    path('files/upload/', upload_file_and_read_text),
    path('files/download/<int:text_id>/', download_text_as_file),
    path('files/generate/', generate_file_from_text),
]
