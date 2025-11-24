from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)

