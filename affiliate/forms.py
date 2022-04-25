from django import forms

from .models import Shortener

class ShortenerForm(forms.ModelForm):
  
    class Meta:
        model = Shortener
        fields = ['long_url']
