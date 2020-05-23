from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Song, Ratings, Scores

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

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
