import os
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Sermon, SermonCategory


class SermonCategorySerializer(serializers.ModelSerializer):
    sermon_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SermonCategory
        fields = ['id', 'name', 'description', 'sermon_count', 'created_at']
    
    def get_sermon_count(self, obj):
        return obj.sermons.filter(is_published=True).count()


class SermonSerializer(serializers.ModelSerializer):
    """Serializer for the Sermon model with audio file handling."""
    # Read-only fields
    audio_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    file_size_mb = serializers.SerializerMethodField()
    processing_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Sermon
        fields = [
            'id', 'title', 'slug', 'sermon_type', 'preacher', 'description', 
            'category', 'category_name', 'playlist', 'audio_file', 'audio_url',
            'thumbnail', 'thumbnail_url', 'bible_references', 'sermon_date',
            'duration', 'duration_display', 'play_count', 'download_count',
            'is_featured', 'is_published', 'order', 'processing_status',
            'processing_errors', 'file_size_mb', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'slug', 'duration', 'play_count', 'download_count', 'created_at', 
            'updated_at', 'processing_status', 'processing_errors'
        ]
        extra_kwargs = {
            'audio_file': {
                'write_only': True,
                'required': False,
                'allow_null': True,
                'help_text': 'Upload an audio file (MP3, WAV, M4A, OGG). Max 100MB.'
            },
            'sermon_date': {'format': '%Y-%m-%d'},
        }
    
    def get_audio_url(self, obj):
        """Return the Cloudinary audio URL"""
        return obj.get_audio_url() if obj.audio_file else None
    
    def get_thumbnail_url(self, obj):
        """Return the Cloudinary thumbnail URL"""
        return obj.thumbnail.url if obj.thumbnail else None
        
    def get_file_size_mb(self, obj):
        """Return file size in MB"""
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return None
    
    def validate_audio_file(self, value):
        """Validate the uploaded audio file."""
        if not value:
            return value
            
        # File size validation (100MB max)
        max_size = 100 * 1024 * 1024  # 100MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f'File too large. Maximum size is 100MB. Your file is {value.size / (1024 * 1024):.2f}MB.'
            )
        
        # File type validation
        valid_mime_types = [
            'audio/mpeg',      # MP3
            'audio/wav',       # WAV
            'audio/wave',      # WAV
            'audio/x-wav',     # WAV
            'audio/mp4',       # M4A
            'audio/x-m4a',     # M4A
            'audio/ogg',       # OGG
            'audio/vorbis',    # OGG
            'audio/opus'       # OGG/OPUS
        ]
        
        # Get file extension
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.opus']
        
        # Check both MIME type and extension
        if (hasattr(value, 'content_type') and 
            value.content_type not in valid_mime_types and
            ext not in valid_extensions):
            raise serializers.ValidationError(
                'Unsupported file type. Supported formats: MP3, WAV, M4A, OGG, OPUS.'
            )
            
        return value
    
    def validate(self, data):
        """Object-level validation."""
        # Ensure either audio_file or soundcloud_embed is provided
        if not data.get('audio_file') and not data.get('soundcloud_embed'):
            raise serializers.ValidationError({
                'audio_file': 'Either audio file or SoundCloud embed is required.',
                'soundcloud_embed': 'Either audio file or SoundCloud embed is required.'
            })
            
        return data
    
    def create(self, validated_data):
        """Handle file upload and processing."""
        # The actual file processing is handled in the model's save() method
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Handle file updates and processing."""
        # The actual file processing is handled in the model's save() method
        return super().update(instance, validated_data)


class SermonListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views with essential fields."""
    audio_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    
    class Meta:
        model = Sermon
        fields = [
            'id', 'title', 'slug', 'preacher', 'sermon_type',
            'category_name', 'audio_url', 'thumbnail_url', 
            'sermon_date', 'duration', 'duration_display',
            'play_count', 'download_count', 'is_featured',
            'is_published', 'created_at'
        ]
        read_only_fields = fields
    
    def get_audio_url(self, obj):
        """Return the Cloudinary audio URL"""
        return obj.get_audio_url() if obj.audio_file else None
    
    def get_thumbnail_url(self, obj):
        """Return the Cloudinary thumbnail URL"""
        return obj.thumbnail.url if obj.thumbnail else None