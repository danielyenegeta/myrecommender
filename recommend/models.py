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
    newsongs = models.ManyToManyField(Song, related_name='newsongs')
    def __str__(self):
        return self.email

class Ratings(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    song = models.ForeignKey(Song, on_delete=models.PROTECT)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

class Scores(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='sheetmusic', null=True, blank=True)
