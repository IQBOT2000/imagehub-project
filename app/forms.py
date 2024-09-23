from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'description', 'category']


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['description']
