from django.contrib import admin
from django.utils.html import format_html
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'event_type', 
        'category', 
        'event_date', 
        'location_short',
        'featured',
        'upcoming'
    )
    list_filter = ('event_type', 'category', 'featured', 'upcoming', 'event_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('featured',)
    date_hierarchy = 'event_date'
    ordering = ('-event_date',)
    readonly_fields = ('event_type', 'upcoming')  # Make these read-only to prevent manual changes
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Date & Time', {
            'fields': ('event_date', 'end_date')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Media', {
            'fields': ('image', 'youtube_link')
        }),
        ('Status', {
            'fields': ('featured', 'event_type', 'upcoming'),
            'description': 'Event type and upcoming status are automatically set based on event_date'
        }),
    )
    
    def location_short(self, obj):
        """Display a shortened version of the location"""
        return obj.location[:50] + '...' if len(obj.location) > 50 else obj.location
    location_short.short_description = 'Location'
    
    def get_queryset(self, request):
        """Ensure event_type and upcoming are synced when viewing the admin list"""
        qs = super().get_queryset(request)
        # Force save on each event to sync the fields
        for event in qs:
            event.save()
        return qs
