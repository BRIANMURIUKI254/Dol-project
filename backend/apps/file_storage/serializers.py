"""
File Storage Serializers

This module contains serializers for the file storage API endpoints.
"""

from rest_framework import serializers
from .models import StoredFile


class StoredFileSerializer(serializers.ModelSerializer):
    """
    Serializer for StoredFile model.
    
    Provides serialization for file metadata and URLs.
    """
    
    file_extension = serializers.ReadOnlyField()
    is_image = serializers.ReadOnlyField()
    is_video = serializers.ReadOnlyField()
    is_document = serializers.ReadOnlyField()
    absolute_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.SerializerMethodField()
    
    class Meta:
        model = StoredFile
        fields = [
            'file_id',
            'file_name',
            'file_reference',
            'mime_type',
            'storage_location',
            'file_url',
            'file_size',
            'uploaded_at',
            'uploaded_by',
            'uploaded_by_username',
            'is_public',
            'description',
            'file_extension',
            'is_image',
            'is_video',
            'is_document',
            'absolute_url',
            'download_url',
        ]
        read_only_fields = [
            'file_id',
            'file_reference',
            'uploaded_at',
            'uploaded_by',
        ]
    
    def get_absolute_url(self, obj):
        """Get the absolute URL for the file."""
        return obj.get_absolute_url()
    
    def get_download_url(self, obj):
        """Get the download URL for the file."""
        return obj.get_download_url()
    
    def get_uploaded_by_username(self, obj):
        """Get the username of the user who uploaded the file."""
        return obj.uploaded_by.username if obj.uploaded_by else None


class FileUploadSerializer(serializers.Serializer):
    """
    Serializer for file upload requests.
    
    Handles file validation and metadata extraction.
    """
    
    file = serializers.FileField(
        help_text="The file to upload"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1000,
        help_text="Optional description of the file"
    )
    is_public = serializers.BooleanField(
        default=True,
        help_text="Whether the file should be publicly accessible"
    )
    
    def validate_file(self, value):
        """
        Validate the uploaded file.
        
        Checks file size, type, and other constraints.
        """
        # Maximum file size: 50MB
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size cannot exceed {max_size // (1024*1024)}MB"
            )
        
        # Check file extension
        allowed_extensions = {
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
            # Videos
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt',
            # Archives
            '.zip', '.rar', '.7z', '.tar', '.gz',
        }
        
        file_extension = value.name.lower().split('.')[-1] if '.' in value.name else ''
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type '.{file_extension}' is not allowed. "
                f"Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return value


class FileResponseSerializer(serializers.Serializer):
    """
    Serializer for file upload response.
    
    Returns file metadata after successful upload.
    """
    
    success = serializers.BooleanField()
    message = serializers.CharField()
    file_data = StoredFileSerializer(required=False)
    file_reference = serializers.UUIDField(required=False)
    file_url = serializers.URLField(required=False)
    errors = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


class FileListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for file lists.
    
    Used when listing multiple files to reduce payload size.
    """
    
    uploaded_by_username = serializers.SerializerMethodField()
    
    class Meta:
        model = StoredFile
        fields = [
            'file_id',
            'file_name',
            'file_reference',
            'mime_type',
            'storage_location',
            'file_size',
            'uploaded_at',
            'uploaded_by_username',
            'is_public',
        ]
    
    def get_uploaded_by_username(self, obj):
        """Get the username of the user who uploaded the file."""
        return obj.uploaded_by.username if obj.uploaded_by else None
