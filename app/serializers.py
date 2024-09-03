from rest_framework import serializers

from .models import Category
from .models import Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'description', 'category', 'user', 'delete', 'uploaded_at', 'updated_at', 'deleted_at']
