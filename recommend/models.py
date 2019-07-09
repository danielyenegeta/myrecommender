from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, default="")
    songs = models.ManyToManyField(Song)
    def __str__(self):
        return self.email
