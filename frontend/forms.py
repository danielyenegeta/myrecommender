from django import forms
from django.core.exceptions import ValidationError
from recommend.models import CustomUser, Song, Ratings

class AddSongForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('songs', 'newsongs',)

class RemoveSongForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('songs',)

class RateSongForm(forms.ModelForm):

    class Meta:
        model = Ratings
        fields = ('person', 'rating',)
