from django import forms
from rest_framework.authtoken.admin import User

from .models import Image


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'description']
