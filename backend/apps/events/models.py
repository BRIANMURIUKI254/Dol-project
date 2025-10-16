from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from apps.core.models import TimeStampedModel


class EventCategory(TimeStampedModel):
    """Model for event categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Event Categories'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Event(TimeStampedModel):
    """Model for ministry events"""
    EVENT_TYPES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='upcoming',
        help_text="Whether the event is upcoming or past"
    )
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Event category'
    )
    event_date = models.DateTimeField(help_text="Date and time of the event")
    end_date = models.DateTimeField(
        null=True, 
        blank=True,
    )
    location = models.TextField(help_text="Event venue or location details")
    image = CloudinaryField('event_images')
    youtube_link = models.URLField(
        blank=True, 
        help_text="Link to event recording or promo video"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Featured events appear in special sections"
    )
    upcoming = models.BooleanField(
        default=True,
        help_text="Automatically set based on event_date"
    )
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        """Override save method to automatically sync event_type and upcoming based on event_date"""
        if self.event_date:
            now = timezone.now()
            if self.event_date > now:
                self.event_type = 'upcoming'
                self.upcoming = True
            else:
                self.event_type = 'past'
                self.upcoming = False
        super().save(*args, **kwargs)
    
    @property
    def is_upcoming(self):
        """Check if the event is upcoming"""
        now = timezone.now()
        return self.event_date > now
    
    @property
    def duration(self):
        """Calculate event duration as timedelta"""
        if self.end_date:
            return self.end_date - self.event_date
        return None
