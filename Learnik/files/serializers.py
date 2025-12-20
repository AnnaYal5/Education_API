from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text='Виберіть файл для завантаження')


class TextGenerationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, default='Untitled', help_text='Назва файлу')
    text = serializers.CharField(help_text='Текст для генерування файлу')
    file_type = serializers.ChoiceField(
        choices=['pdf', 'docx', 'txt'], 
        default='pdf',
        help_text='Формат файлу'
    )


class FileResponseSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    filename = serializers.CharField()


class TextResponseSerializer(serializers.Serializer):
    text = serializers.CharField()