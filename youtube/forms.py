from django import forms
from django.core.validators import RegexValidator
url_validator = RegexValidator(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', 'Only youtube url')

class YoutubeForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'type': 'url', 'placeholder': 'Enter url:', 'class': 'form-control', 'name': 'url', 'id': 'id_url', 'required': 'required'}), validators=[url_validator])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'name': 'email', 'id': 'id_email', 'required': 'required'}))