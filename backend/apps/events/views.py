from django.utils import timezone
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event
from .serializers import EventSerializer
from apps.core.permissions import IsAdminOrReadOnly


class EventListView(generics.ListCreateAPIView):
    """View to list and create events"""
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'category', 'featured']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['-event_date']
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by upcoming/past events if specified
        event_filter = self.request.query_params.get('filter', None)
        if event_filter == 'upcoming':
            queryset = queryset.filter(event_date__gte=timezone.now())
        elif event_filter == 'past':
            queryset = queryset.filter(event_date__lt=timezone.now())
            
        return queryset


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete an event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'


class FeaturedEventsView(generics.ListAPIView):
    """View to list featured events"""
    serializer_class = EventSerializer
    
    def get_queryset(self):
        return Event.objects.filter(
            featured=True,
            event_date__gte=timezone.now()
        ).order_by('event_date')[:3]  # Limit to 3 featured events
