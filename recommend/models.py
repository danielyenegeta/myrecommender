from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    def __str__(self):
        return self.email

class Song(models.Model):
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
