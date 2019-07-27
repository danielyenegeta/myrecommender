from django import forms
from django.core.exceptions import ValidationError
from recommend.models import CustomUser, Song, Ratings

class AddSongForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddSongForm,self).__init__(*args,**kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. As'
        self.fields['artist'].widget.attrs['placeholder'] = 'e.g. Stevie Wonder'

    class Meta:
        model = Song
        fields = ('title', 'artist')

class RemoveSongForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('songs',)

class RateSongForm(forms.ModelForm):

    class Meta:
        model = Ratings
        fields = ('person', 'rating',)
