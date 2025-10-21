"""
File Storage Admin Configuration

This module configures the Django admin interface for file storage.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import StoredFile


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for StoredFile model.
    """
    
    list_display = [
        'file_id',
        'file_name',
        'storage_location',
        'mime_type',
        'file_size_display',
        'uploaded_by',
        'uploaded_at',
        'is_public',
        'file_url_link',
    ]
    
    list_filter = [
        'storage_location',
        'mime_type',
        'is_public',
        'uploaded_at',
        'uploaded_by',
    ]
    
    search_fields = [
        'file_name',
        'file_reference',
        'description',
        'uploaded_by__username',
        'uploaded_by__email',
    ]
    
    readonly_fields = [
        'file_id',
        'file_reference',
        'uploaded_at',
        'file_url_link',
        'file_preview',
    ]
    
    fieldsets = (
        ('File Information', {
            'fields': (
                'file_id',
                'file_name',
                'file_reference',
                'mime_type',
                'file_size',
                'storage_location',
            )
        }),
        ('Storage Details', {
            'fields': (
                'file_url',
                'file_url_link',
                'file_preview',
            )
        }),
        ('Access Control', {
            'fields': (
                'is_public',
                'uploaded_by',
            )
        }),
        ('Metadata', {
            'fields': (
                'description',
                'uploaded_at',
            )
        }),
    )
    
    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size:
            size = obj.file_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "Unknown"
    file_size_display.short_description = "File Size"
    
    def file_url_link(self, obj):
        """Display file URL as a clickable link."""
        if obj.file_url:
            if obj.storage_location == 'cloudinary':
                return format_html(
                    '<a href="{}" target="_blank">View on Cloudinary</a>',
                    obj.file_url
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank">View File</a>',
                    obj.file_url
                )
        return "No URL"
    file_url_link.short_description = "File URL"
    
    def file_preview(self, obj):
        """Show file preview for images."""
        if obj.is_image and obj.file_url:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.file_url
            )
        elif obj.is_video and obj.file_url:
            return format_html(
                '<video controls style="max-width: 200px; max-height: 200px;">'
                '<source src="{}" type="{}">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.file_url,
                obj.mime_type
            )
        return "No preview available"
    file_preview.short_description = "Preview"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('uploaded_by')
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion only for superusers or file owners."""
        if obj is None:
            return request.user.is_superuser
        return (
            request.user.is_superuser or
            (obj.uploaded_by and obj.uploaded_by == request.user)
        )
    
    def save_model(self, request, obj, form, change):
        """Set uploaded_by if not set and user is authenticated."""
        if not change and not obj.uploaded_by and request.user.is_authenticated:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
