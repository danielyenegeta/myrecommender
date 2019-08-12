from django.contrib import admin
from .models import Song, Ratings, Scores, CustomUser

# Register your models here.

admin.site.register(Song)
admin.site.register(Ratings)
admin.site.register(Scores)
admin.site.register(CustomUser)
