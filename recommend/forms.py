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
