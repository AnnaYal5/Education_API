from django.db import models

class GeneratedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="generated/")
    file_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class TextStorage(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TextStorage {self.id}"