from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter, orderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Sermon, SermonCategory
from .serializers import (
    SermonSerializer, 
    SermonListSerializer,
    SermonCategorySerializer
)


class SermonViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing sermons.
    """
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, orderingFilter]
    filterset_fields = [
        'category', 'preacher', 'sermon_type', 
        'is_published', 'is_featured'
    ]
    search_fields = ['title', 'preacher', 'description', 'bible_references']
    ordering_fields = ['-created_at', 'title', 'sermon_date', 'play_count']
    ordering = ['-sermon_date', '-created_at']
    
    def get_queryset(self):
        """
        Optionally filter by published status for non-staff users.
        """
        queryset = super().get_queryset()
        
        # For non-staff users, only show published sermons
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
            
        # Annotate with like and comment counts
        queryset = queryset.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        
        return queryset
        
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return SermonListSerializer
        return SermonSerializer
    
    @action(detail=True, methods=['post'])
    def increment_play_count(self, request, pk=None):
        """Increment the play count for a sermon."""
        sermon = self.get_object()
        sermon.increment_play_count()
        return Response({'status': 'play count incremented'})
    
    @action(detail=True, methods=['post'])
    def increment_download_count(self, request, pk=None):
        """Increment the download count for a sermon."""
        sermon = self.get_object()
        sermon.increment_download_count()
        return Response({'status': 'download count incremented'})
    
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        """Toggle the featured status of a sermon (admin only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        sermon = self.get_object()
        sermon.is_featured = not sermon.is_featured
        sermon.save()
        
        return Response({
            'status': 'success',
            'is_featured': sermon.is_featured
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent sermons with pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured sermons."""
        queryset = self.filter_queryset(
            self.get_queryset().filter(is_featured=True)
        )
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SermonCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing sermon categories.
    """
    queryset = SermonCategory.objects.all()
    serializer_class = SermonCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    
    @action(detail=True, methods=['get'])
    def sermons(self, request, pk=None):
        """Get all sermons in this category."""
        category = self.get_object()
        sermons = category.sermons.all()
        
        # Apply filtering, searching, and ordering
        sermons = SermonViewSet.filter_queryset(
            self.request, 
            sermons, 
            SermonViewSet
        )
        
        # Paginate the results
        page = self.paginate_queryset(sermons)
        if page is not None:
            serializer = SermonListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = SermonListSerializer(sermons, many=True)
        return Response(serializer.data)