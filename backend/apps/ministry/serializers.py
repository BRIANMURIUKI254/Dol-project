from rest_framework import serializers
from .models import MinistryInfo, SocialMedia, CarouselImage


class CarouselImageSerializer(serializers.ModelSerializer):
    """Serializer for carousel images"""
    class Meta:
        model = CarouselImage
        fields = ('id', 'image', 'caption', 'order', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')


class SocialMediaSerializer(serializers.ModelSerializer):
    """Serializer for social media links"""
    class Meta:
        model = SocialMedia
        fields = ('telegram', 'instagram', 'facebook', 'youtube', 'spotify', 'app_store', 'email', 'phone_number')


class MinistryInfoSerializer(serializers.ModelSerializer):
    """Serializer for ministry information"""
    social_media = SocialMediaSerializer(read_only=True)
    carousel_images = CarouselImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = MinistryInfo
        fields = (
            'lead_steward_name',
            'lead_steward_title',
            'lead_steward_bio',
            'lead_steward_image',
            'about_text',
            'history_text',
            'vision',
            'mission',
            'ministry_verses',
            'social_media',
            'carousel_images',
            'updated_at'
        )
        read_only_fields = ('updated_at',)
