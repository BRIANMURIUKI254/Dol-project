"""
File Storage Models

This module contains the StoredFile model for managing file uploads
with support for both local storage and Cloudinary.
"""

import uuid
import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class StoredFile(models.Model):
    """
    Model for storing file metadata and references.
    
    Supports both local storage and Cloudinary storage based on file type.
    Images and videos are stored on Cloudinary, while documents are stored locally.
    """
    
    STORAGE_CHOICES = [
        ('local', 'Local Storage'),
        ('cloudinary', 'Cloudinary'),
    ]
    
    # Primary key
    file_id = models.AutoField(primary_key=True)
    
    # File information
    file_name = models.CharField(
        max_length=255,
        help_text="Original name of the uploaded file"
    )
    
    file_reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="Unique reference for file lookups"
    )
    
    mime_type = models.CharField(
        max_length=100,
        help_text="MIME type of the file (e.g., image/jpeg, application/pdf)"
    )
    
    storage_location = models.CharField(
        max_length=20,
        choices=STORAGE_CHOICES,
        help_text="Where the file is stored (local or cloudinary)"
    )
    
    file_url = models.URLField(
        max_length=500,
        help_text="Full URL or file path to access the file"
    )
    
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Size of the file in bytes"
    )
    
    # Timestamps and user tracking
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the file was uploaded"
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who uploaded the file"
    )
    
    # Additional metadata
    is_public = models.BooleanField(
        default=True,
        help_text="Whether the file is publicly accessible"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Optional description of the file"
    )
    
    class Meta:
        db_table = 'stored_files'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['file_reference']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['storage_location']),
            models.Index(fields=['mime_type']),
        ]
    
    def __str__(self):
        return f"{self.file_name} ({self.storage_location})"
    
    @property
    def file_extension(self):
        """Get the file extension from the file name."""
        return os.path.splitext(self.file_name)[1].lower()
    
    @property
    def is_image(self):
        """Check if the file is an image."""
        return self.mime_type.startswith('image/')
    
    @property
    def is_video(self):
        """Check if the file is a video."""
        return self.mime_type.startswith('video/')
    
    @property
    def is_document(self):
        """Check if the file is a document (PDF, DOC, etc.)."""
        document_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/plain',
        ]
        return self.mime_type in document_types
    
    def get_absolute_url(self):
        """Get the absolute URL for accessing this file."""
        return f"/api/files/{self.file_reference}/"
    
    def get_download_url(self):
        """Get the download URL for this file."""
        return f"/api/files/{self.file_reference}/download/"
