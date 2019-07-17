from rest_framework import serializers
from .models import Song, CustomUser, Ratings, Scores

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'artist')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'songs', 'recommends', 'newsongs')

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('person', 'song', 'rating')

class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = ('song', 'pdf')
