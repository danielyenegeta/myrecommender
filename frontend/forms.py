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

class RateSongForm(forms.ModelForm):

    class Meta:
        model = Ratings
        fields = ('person', 'rating',)
