from django.urls import path
from . import views

urlpatterns = [
    path('files/<int:file_id>/content/', views.get_file_content, name='file-content'),
]
