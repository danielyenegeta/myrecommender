from rest_framework import serializers
from recommend.models import *

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'

class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = '__all__'
