from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Category


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'file', 'description', 'category', 'user', 'delete',
        'uploaded_at', 'updated_at', 'deleted_at'
    )
    list_filter = ('category', 'user', 'delete', 'uploaded_at')
    search_fields = ('description', 'category__name')
    list_per_page = 20

    def image_thumbnail(self, obj):
        if obj.file:
            return format_html('<img src="{}" width="100" height="100" />', obj.file.url)
        return 'No Image'

    image_thumbnail.short_description = 'Thumbnail'
    list_display = (
        'id', 'image_thumbnail', 'description', 'category', 'user', 'delete', 'uploaded_at', 'updated_at', 'deleted_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_per_page = 20
