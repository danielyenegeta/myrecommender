from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, default="")
    songs = models.ManyToManyField(Song)
    recommends = models.ManyToManyField(Song, related_name='user_recommends', through='Ratings')
    def __str__(self):
        return self.email

class Ratings(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
