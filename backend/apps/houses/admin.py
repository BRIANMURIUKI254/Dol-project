from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'meeting_day', 'start_time', 'end_time', 'is_active', 'order')
    list_filter = ('meeting_day', 'is_active')
    search_fields = ('name', 'location', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active', 'order')
        }),
        ('Meeting Details', {
            'fields': ('meeting_day', 'start_time', 'end_time')
        }),
        ('Location', {
            'fields': ('location',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', 'name')
