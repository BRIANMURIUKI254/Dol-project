from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

from apps.core.models import TimeStampedModel

class MinistryInfo(TimeStampedModel):
    """Singleton model for ministry information"""
    lead_steward_name = models.CharField(max_length=100, default='Pst Kelvin Muli')
    lead_steward_title = models.CharField(max_length=100, default='Lead Steward')
    lead_steward_bio = RichTextField(blank=True)
    lead_steward_image = CloudinaryField('ministry_leaders', blank=True, null=True)
    history_text = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    ministry_verses = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ministry Information'
        verbose_name_plural = 'Ministry Information'
    
    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure singleton
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass  # Prevent deletion
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SocialMedia(models.Model):
    """Singleton model for social media links"""
    telegram = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    spotify = models.URLField(blank=True)
    app_store = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Social Media Links'
        verbose_name_plural = 'Social Media Links'
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class CarouselImage(models.Model):
    """Model for carousel images on the homepage"""
    image = CloudinaryField('carousel_images')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'
    
    def __str__(self):
        return f"Carousel Image {self.order}"
