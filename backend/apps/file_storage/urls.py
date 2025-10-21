"""
File Storage URL Configuration

This module defines URL patterns for file storage API endpoints.
"""

from django.urls import path
from . import views

app_name = 'file_storage'

urlpatterns = [
    # File upload endpoint
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    
    # File retrieval endpoints
    path('files/<uuid:file_reference>/', views.get_file_by_reference, name='get_file'),
    path('files/<uuid:file_reference>/serve/', views.serve_file, name='serve_file'),
    
    # File management endpoints
    path('files/', views.list_user_files, name='list_user_files'),
    path('files/<uuid:file_reference>/delete/', views.delete_file, name='delete_file'),
    
    # Statistics endpoint
    path('stats/', views.file_stats, name='file_stats'),
]
