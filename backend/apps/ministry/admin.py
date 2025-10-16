from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MinistryInfo, SocialMedia, CarouselImage


@admin.register(MinistryInfo)
class MinistryInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Lead Steward Information', {
            'fields': (
                'lead_steward_name', 
                'lead_steward_title', 
                'lead_steward_bio', 
                'lead_steward_image'
            )
        }),
        ('Ministry Content', {
            'fields': (
                'about_text', 
                'history_text', 
                'vision', 
                'mission', 
                'ministry_verses'
            )
        }),
    )
    
    def has_add_permission(self, request):
        return not MinistryInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number')
    
    def has_add_permission(self, request):
        return not SocialMedia.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('caption',)
    ordering = ('order', 'created_at')
