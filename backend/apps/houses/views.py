from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import House
from .serializers import HouseSerializer
from apps.core.permissions import IsAdminOrReadOnly


class HouseListView(generics.ListCreateAPIView):
    """View to list and create houses"""
    queryset = House.objects.filter(is_active=True).order_by('order', 'name')
    serializer_class = HouseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['meeting_day', 'is_active']
    search_fields = ['name', 'location', 'description']
    ordering_fields = ['order', 'name', 'meeting_day']
    ordering = ['order', 'name']


class HouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a house"""
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'
    
    def perform_destroy(self, instance):
        # Soft delete by setting is_active to False
        instance.is_active = False
        instance.save()
