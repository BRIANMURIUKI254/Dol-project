"""
File Storage Utilities

This module contains utility functions for file handling,
storage decisions, and file operations.
"""

import os
import uuid
import mimetypes
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import cloudinary.api


def get_file_mime_type(file):
    """
    Get the MIME type of a file.
    
    Args:
        file: Django UploadedFile object
        
    Returns:
        str: MIME type of the file
    """
    # First try to get from the file's content_type
    if hasattr(file, 'content_type') and file.content_type:
        return file.content_type
    
    # Fallback to mimetypes module
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type:
        return mime_type
    
    # Default fallback
    return 'application/octet-stream'


def determine_storage_location(mime_type):
    """
    Determine where a file should be stored based on its MIME type.
    
    Args:
        mime_type (str): MIME type of the file
        
    Returns:
        str: 'cloudinary' for images/videos, 'local' for documents
    """
    # Images and videos go to Cloudinary
    if mime_type.startswith(('image/', 'video/')):
        return 'cloudinary'
    
    # Everything else goes to local storage
    return 'local'


def generate_local_file_path(file_name, year=None, month=None):
    """
    Generate a local file path for storing files.
    
    Args:
        file_name (str): Original file name
        year (int, optional): Year for directory structure
        month (int, optional): Month for directory structure
        
    Returns:
        str: Relative file path
    """
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    # Create directory structure: uploads/YYYY/MM/
    directory = f"uploads/{year}/{month:02d}"
    
    # Generate unique filename to avoid conflicts
    file_extension = os.path.splitext(file_name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    return os.path.join(directory, unique_filename)


def upload_to_cloudinary(file, public_id=None, folder="dol_uploads"):
    """
    Upload a file to Cloudinary.
    
    Args:
        file: Django UploadedFile object
        public_id (str, optional): Custom public ID for the file
        folder (str): Cloudinary folder to store the file
        
    Returns:
        dict: Cloudinary upload response with URL and metadata
    """
    try:
        # Generate public_id if not provided
        if not public_id:
            file_extension = os.path.splitext(file.name)[1]
            public_id = f"{folder}/{uuid.uuid4()}"
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            folder=folder,
            resource_type="auto",  # Automatically detect image/video/raw
            overwrite=True,
            invalidate=True,
        )
        
        return upload_result
        
    except Exception as e:
        raise Exception(f"Cloudinary upload failed: {str(e)}")


def upload_to_local_storage(file, file_path):
    """
    Upload a file to local storage.
    
    Args:
        file: Django UploadedFile object
        file_path (str): Path where to store the file
        
    Returns:
        str: URL to access the stored file
    """
    try:
        # Save file to local storage
        saved_path = default_storage.save(file_path, ContentFile(file.read()))
        
        # Generate URL for accessing the file
        file_url = default_storage.url(saved_path)
        
        return file_url
        
    except Exception as e:
        raise Exception(f"Local storage upload failed: {str(e)}")


def validate_file_type(file):
    """
    Validate if a file type is allowed.
    
    Args:
        file: Django UploadedFile object
        
    Returns:
        bool: True if file type is allowed
    """
    allowed_mime_types = {
        # Images
        'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp',
        'image/webp', 'image/svg+xml',
        # Videos
        'video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/flv',
        'video/webm', 'video/quicktime', 'video/x-msvideo',
        # Documents
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'text/plain',
        # Archives
        'application/zip',
        'application/x-rar-compressed',
        'application/x-7z-compressed',
        'application/x-tar',
        'application/gzip',
    }
    
    mime_type = get_file_mime_type(file)
    return mime_type in allowed_mime_types


def validate_file_size(file, max_size_mb=50):
    """
    Validate if a file size is within limits.
    
    Args:
        file: Django UploadedFile object
        max_size_mb (int): Maximum file size in MB
        
    Returns:
        bool: True if file size is within limits
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file.size <= max_size_bytes


def get_file_info(file):
    """
    Extract file information from an uploaded file.
    
    Args:
        file: Django UploadedFile object
        
    Returns:
        dict: File information including name, size, MIME type, etc.
    """
    return {
        'name': file.name,
        'size': file.size,
        'mime_type': get_file_mime_type(file),
        'extension': os.path.splitext(file.name)[1].lower(),
    }


def delete_cloudinary_file(public_id):
    """
    Delete a file from Cloudinary.
    
    Args:
        public_id (str): Cloudinary public ID of the file to delete
        
    Returns:
        bool: True if deletion was successful
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        print(f"Error deleting Cloudinary file {public_id}: {str(e)}")
        return False


def delete_local_file(file_path):
    """
    Delete a file from local storage.
    
    Args:
        file_path (str): Path to the file to delete
        
    Returns:
        bool: True if deletion was successful
    """
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting local file {file_path}: {str(e)}")
        return False


def get_cloudinary_public_id_from_url(url):
    """
    Extract Cloudinary public ID from a URL.
    
    Args:
        url (str): Cloudinary URL
        
    Returns:
        str: Public ID or None if not a Cloudinary URL
    """
    try:
        # Cloudinary URLs typically look like:
        # https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
        if 'cloudinary.com' in url:
            parts = url.split('/')
            # Find the upload part and get everything after it
            upload_index = parts.index('upload')
            if upload_index + 1 < len(parts):
                public_id_with_version = '/'.join(parts[upload_index + 2:])
                # Remove version prefix if present
                if public_id_with_version.startswith('v'):
                    public_id_with_version = public_id_with_version.split('/', 1)[1]
                # Remove file extension
                public_id = os.path.splitext(public_id_with_version)[0]
                return public_id
    except (ValueError, IndexError):
        pass
    
    return None
