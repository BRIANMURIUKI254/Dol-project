from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class House(TimeStampedModel):
    """Model for houses where meetings are held"""
    DAYS_OF_WEEK = [
        ('monday', _('Monday')),
        ('tuesday', _('Tuesday')),
        ('wednesday', _('Wednesday')),
        ('thursday', _('Thursday')),
        ('friday', _('Friday')),
        ('saturday', _('Saturday')),
        ('sunday', _('Sunday')),
    ]
    
    name = models.CharField(max_length=100)
    location = models.TextField(help_text="Detailed address of the house")
    meeting_day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, help_text="Additional information about the house")
    is_active = models.BooleanField(default=True, help_text="Whether this house is currently active")
    order = models.IntegerField(
        default=0, 
        help_text="Order in which the house appears in listings"
    )
    
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
    
    def __str__(self):
        return f"{self.name} - {self.get_meeting_day_display()}"
    
    @property
    def meeting_schedule(self):
        """Returns a formatted meeting schedule string"""
        return f"{self.get_meeting_day_display()}s, {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
