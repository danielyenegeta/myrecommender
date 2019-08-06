from django import forms
from django.core.exceptions import ValidationError
from recommend.models import CustomUser, Song, Ratings

class AddSongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ('title', 'artist')

class RemoveSongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ('title', 'artist')

class RateSongForm(forms.Form):
    song = forms.CharField(max_length=50)
    artist = forms.CharField(max_length=50)
    rating = forms.IntegerField(min_value=0, max_value=5)
