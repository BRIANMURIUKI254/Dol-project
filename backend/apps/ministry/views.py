from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import MinistryInfo, SocialMedia, CarouselImage
from .serializers import MinistryInfoSerializer, CarouselImageSerializer
from apps.core.permissions import IsAdminOrReadOnly


class MinistryInfoView(generics.RetrieveAPIView):
    """View to retrieve ministry information"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MinistryInfoSerializer
    
    def get_object(self):
        # Return the singleton instance
        return MinistryInfo.load()


class CarouselImageView(generics.ListCreateAPIView):
    """View to list and create carousel images"""
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CarouselImageSerializer
    queryset = CarouselImage.objects.filter(is_active=True).order_by('order')
    
    def perform_create(self, serializer):
        serializer.save()


class CarouselImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a carousel image"""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CarouselImageSerializer
    queryset = CarouselImage.objects.all()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        # Soft delete by setting is_active to False
        instance.is_active = False
        instance.save()
