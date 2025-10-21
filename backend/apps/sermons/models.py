import os
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from apps.core.models import TimeStampedField

class TimeStampedModel(models.Model):
    """Abstract base class with self-updating created and modified fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SermonCategory(TimeStampedModel):
    """Model for categorizing sermons"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    thumbnail = CloudinaryField(
        'category_thumbnails',
        blank=True,
        null=True,
        help_text="Thumbnail image for the category"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(
        default=0,
        help_text="Order in which the category appears in listings"
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Sermon Category'
        verbose_name_plural = 'Sermon Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Playlist(TimeStampedModel):
    """Model for sermon playlists or series"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = CloudinaryField('sermon_thumbnails', blank=True, null=True)
    order = models.IntegerField(
        default=0,
        help_text="Order in which the playlist appears in listings"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
    
    def __str__(self):
        return self.name
    
    @property
    def sermon_count(self):
        """Return the number of sermons in this playlist"""
        return self.sermons.count()


class Sermon(TimeStampedModel):
    """Model for sermon messages with audio files"""
    AUDIO_TYPES = (
        ('sermon', 'Sermon'),
        ('bible_study', 'Bible Study'),
        ('devotional', 'Devotional'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    sermon_type = models.CharField(
        max_length=20,
        choices=AUDIO_TYPES,
        default='sermon',
        help_text="Type of audio content"
    )
    preacher = models.CharField(max_length=100)
    sermon_date = models.DateField(help_text="Date the sermon was delivered")
    
    category = models.ForeignKey(
        SermonCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sermons',
        help_text="The category this sermon belongs to"
    )
    
    playlist = models.ForeignKey(
        'sermons.Playlist', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sermons',
        help_text="The playlist this sermon belongs to"
    )
    
    duration = models.PositiveIntegerField(
        default=0,
        help_text="Duration in seconds"
    )
    
    audio_file = CloudinaryField(
        'sermon_audio',
        resource_type='video',  # Required for audio files in Cloudinary
        blank=True,
        null=True,
        help_text="Upload audio file (MP3, WAV, M4A, OGG). Max 100MB"
    )
    
    # Audio metadata
    file_size = models.PositiveBigIntegerField(
        default=0,
        help_text="File size in bytes"
    )
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Detected MIME type of the audio file"
    )
    
    soundcloud_embed = models.URLField(
        blank=True,
        help_text="SoundCloud embed URL if hosted externally"
    )
    
    thumbnail = CloudinaryField(
        'sermon_thumbnails',
        blank=True,
        null=True,
        help_text="Custom thumbnail image for the sermon (16:9 aspect ratio recommended)"
    )
    
    bible_references = models.TextField(
        blank=True,
        help_text="Bible references (e.g., John 3:16-17, Romans 8:28-30)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description or notes about the sermon"
    )
    
    # Statistics
    play_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times the sermon has been played"
    )
    
    download_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times the sermon has been downloaded"
    )
    
    # Metadata
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured sermons appear in prominent sections"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which the sermon appears in listings"
    )
    
    is_published = models.BooleanField(
        default=True,
        help_text="Whether the sermon is published and visible to users"
    )
    
    # For error tracking
    processing_status = models.CharField(
        max_length=20,
        default='pending',
        choices=(
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ),
        help_text="Current status of audio processing"
    )
    processing_errors = models.TextField(
        blank=True,
        help_text="Any errors that occurred during processing"
    )
    
    def increment_play_count(self):
        """Increment the play count"""
        self.play_count = models.F('play_count') + 1
        self.save(update_fields=['play_count', 'updated_at'])

    def increment_download_count(self):
        """Increment the download count"""
        self.download_count = models.F('download_count') + 1
        self.save(update_fields=['download_count', 'updated_at'])
        
    def get_audio_url(self):
        """Get the audio URL with Cloudinary transformations if needed"""
        if not self.audio_file:
            return None
            
        # You can add Cloudinary transformations here if needed
        # Example: return self.audio_file.build_url(transformation={
        #     'format': 'mp3',
        #     'quality': 'auto:low',
        #     'bit_rate': '64k'
        # })
        return self.audio_file.url
        
    def get_duration_display(self):
        """Return duration in MM:SS format"""
        if not self.duration:
            return ""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
        
    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Ensure either audio_file or soundcloud_embed is provided
        if not self.audio_file and not self.soundcloud_embed:
            raise ValidationError({
                'audio_file': 'Either audio file or SoundCloud embed is required',
                'soundcloud_embed': 'Either audio file or SoundCloud embed is required'
            })
    
    @property
    def duration_formatted(self):
        """Return duration in HH:MM:SS format"""
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @property
    def audio_url(self):
        """Get the Cloudinary audio URL"""
        if self.audio_file:
            return self.audio_file.url
        return None
    
    @property
    def thumbnail_url(self):
        """Get the Cloudinary thumbnail URL"""
        if self.thumbnail:
            return self.thumbnail.url
        return None