from django.urls import path
from . import views

urlpatterns = [
    path('ai/generate-conspect/', views.create_conspect, name='generate-conspect'),
    path('ai/generate-test/', views.create_test, name='generate-test'),
]
