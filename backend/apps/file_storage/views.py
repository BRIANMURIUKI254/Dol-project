"""
File Storage Views

This module contains API views for file upload, retrieval, and management.
"""

import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import StoredFile
from .serializers import (
    StoredFileSerializer,
    FileUploadSerializer,
    FileResponseSerializer,
    FileListSerializer
)
from .utils import (
    get_file_mime_type,
    determine_storage_location,
    generate_local_file_path,
    upload_to_cloudinary,
    upload_to_local_storage,
    validate_file_type,
    validate_file_size,
    get_file_info,
    delete_cloudinary_file,
    delete_local_file,
    get_cloudinary_public_id_from_url,
)


class FileUploadView(APIView):
    """
    API view for uploading files.
    
    Supports both local storage and Cloudinary based on file type.
    Images and videos are uploaded to Cloudinary, documents to local storage.
    """
    
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handle file upload.
        
        Expected form data:
        - file: The file to upload
        - description: Optional description
        - is_public: Whether file should be public (default: True)
        """
        try:
            # Validate the uploaded file
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Invalid file data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            file = serializer.validated_data['file']
            description = serializer.validated_data.get('description', '')
            is_public = serializer.validated_data.get('is_public', True)
            
            # Validate file type and size
            if not validate_file_type(file):
                return Response({
                    'success': False,
                    'message': 'File type not allowed',
                    'errors': ['Invalid file type']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not validate_file_size(file):
                return Response({
                    'success': False,
                    'message': 'File size exceeds limit',
                    'errors': ['File size cannot exceed 50MB']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get file information
            file_info = get_file_info(file)
            mime_type = file_info['mime_type']
            storage_location = determine_storage_location(mime_type)
            
            # Generate file reference
            file_reference = None
            
            try:
                if storage_location == 'cloudinary':
                    # Upload to Cloudinary
                    upload_result = upload_to_cloudinary(file)
                    file_url = upload_result['secure_url']
                    file_size = upload_result.get('bytes', file.size)
                    
                else:
                    # Upload to local storage
                    file_path = generate_local_file_path(file.name)
                    file_url = upload_to_local_storage(file, file_path)
                    file_size = file.size
                
                # Create database record
                stored_file = StoredFile.objects.create(
                    file_name=file.name,
                    file_reference=file_reference,
                    mime_type=mime_type,
                    storage_location=storage_location,
                    file_url=file_url,
                    file_size=file_size,
                    uploaded_by=request.user,
                    is_public=is_public,
                    description=description,
                )
                
                # Serialize the response
                file_serializer = StoredFileSerializer(stored_file)
                
                return Response({
                    'success': True,
                    'message': 'File uploaded successfully',
                    'file_data': file_serializer.data,
                    'file_reference': str(stored_file.file_reference),
                    'file_url': stored_file.file_url,
                }, status=status.HTTP_201_CREATED)
                
            except Exception as upload_error:
                return Response({
                    'success': False,
                    'message': 'File upload failed',
                    'errors': [str(upload_error)]
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': 'An error occurred during upload',
                'errors': [str(e)]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_file_by_reference(request, file_reference):
    """
    Retrieve file information by file reference.
    
    Returns file metadata and access URL.
    """
    try:
        stored_file = get_object_or_404(StoredFile, file_reference=file_reference)
        
        # Check if file is public or user has access
        if not stored_file.is_public and not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'File is private and requires authentication'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user is the uploader or has admin rights
        if not stored_file.is_public and request.user != stored_file.uploaded_by and not request.user.is_staff:
            return Response({
                'success': False,
                'message': 'Access denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StoredFileSerializer(stored_file)
        
        return Response({
            'success': True,
            'file_data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Http404:
        return Response({
            'success': False,
            'message': 'File not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'An error occurred',
            'errors': [str(e)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def serve_file(request, file_reference):
    """
    Serve file content directly.
    
    For local files, serves the file content.
    For Cloudinary files, redirects to the Cloudinary URL.
    """
    try:
        stored_file = get_object_or_404(StoredFile, file_reference=file_reference)
        
        # Check access permissions
        if not stored_file.is_public and not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'File is private and requires authentication'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not stored_file.is_public and request.user != stored_file.uploaded_by and not request.user.is_staff:
            return Response({
                'success': False,
                'message': 'Access denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if stored_file.storage_location == 'cloudinary':
            # For Cloudinary files, redirect to the URL
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(stored_file.file_url)
        else:
            # For local files, serve the file content
            from django.core.files.storage import default_storage
            from django.http import FileResponse
            
            try:
                # Extract the relative path from the URL
                file_path = stored_file.file_url.replace(settings.MEDIA_URL, '')
                
                if default_storage.exists(file_path):
                    file_obj = default_storage.open(file_path)
                    response = FileResponse(file_obj, content_type=stored_file.mime_type)
                    response['Content-Disposition'] = f'inline; filename="{stored_file.file_name}"'
                    return response
                else:
                    return Response({
                        'success': False,
                        'message': 'File not found on storage'
                    }, status=status.HTTP_404_NOT_FOUND)
                    
            except Exception as e:
                return Response({
                    'success': False,
                    'message': 'Error serving file',
                    'errors': [str(e)]
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    except Http404:
        return Response({
            'success': False,
            'message': 'File not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'An error occurred',
            'errors': [str(e)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_files(request):
    """
    List files uploaded by the current user.
    """
    try:
        files = StoredFile.objects.filter(uploaded_by=request.user)
        
        # Apply filters if provided
        storage_location = request.GET.get('storage_location')
        mime_type = request.GET.get('mime_type')
        is_public = request.GET.get('is_public')
        
        if storage_location:
            files = files.filter(storage_location=storage_location)
        if mime_type:
            files = files.filter(mime_type__startswith=mime_type)
        if is_public is not None:
            files = files.filter(is_public=is_public.lower() == 'true')
        
        serializer = FileListSerializer(files, many=True)
        
        return Response({
            'success': True,
            'files': serializer.data,
            'count': files.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'An error occurred',
            'errors': [str(e)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_reference):
    """
    Delete a file and its database record.
    
    Only the file owner or admin can delete files.
    """
    try:
        stored_file = get_object_or_404(StoredFile, file_reference=file_reference)
        
        # Check if user can delete this file
        if request.user != stored_file.uploaded_by and not request.user.is_staff:
            return Response({
                'success': False,
                'message': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Delete the actual file from storage
        if stored_file.storage_location == 'cloudinary':
            public_id = get_cloudinary_public_id_from_url(stored_file.file_url)
            if public_id:
                delete_cloudinary_file(public_id)
        else:
            # For local files, extract the relative path
            file_path = stored_file.file_url.replace(settings.MEDIA_URL, '')
            delete_local_file(file_path)
        
        # Delete the database record
        stored_file.delete()
        
        return Response({
            'success': True,
            'message': 'File deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Http404:
        return Response({
            'success': False,
            'message': 'File not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'An error occurred',
            'errors': [str(e)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def file_stats(request):
    """
    Get file storage statistics.
    
    Returns counts by storage location and file type.
    """
    try:
        stats = {
            'total_files': StoredFile.objects.count(),
            'by_storage': {
                'local': StoredFile.objects.filter(storage_location='local').count(),
                'cloudinary': StoredFile.objects.filter(storage_location='cloudinary').count(),
            },
            'by_type': {
                'images': StoredFile.objects.filter(mime_type__startswith='image/').count(),
                'videos': StoredFile.objects.filter(mime_type__startswith='video/').count(),
                'documents': StoredFile.objects.filter(
                    mime_type__in=[
                        'application/pdf',
                        'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'text/plain',
                    ]
                ).count(),
            },
            'total_size': sum(
                f.file_size or 0 for f in StoredFile.objects.all()
            ),
        }
        
        return Response({
            'success': True,
            'stats': stats
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'An error occurred',
            'errors': [str(e)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
