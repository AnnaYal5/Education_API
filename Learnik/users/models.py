from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)


class FileLearning(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва файлу")
    file = models.FileField(upload_to='learning_materials/', verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title