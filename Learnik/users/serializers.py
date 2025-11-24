from rest_framework import serializers
from .models import  FileLearning


class LearningFileSerializer(serializers.ModelSerializer):
    class Meta:
        model =  FileLearning
        fields = ('id', 'title', 'file', 'created_at')