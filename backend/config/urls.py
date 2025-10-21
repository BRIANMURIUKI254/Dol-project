"""
URL configuration for Days of Light (D.O.L) ministry backend.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Redirect root to API docs
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),
    
    # API endpoints
    path('api/auth/', include('apps.accounts.urls')),
    path('api/ministry/', include('apps.ministry.urls')),
    path('api/houses/', include('apps.houses.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/giving/', include('apps.giving.urls')),
    path('api/admin/', include('apps.admin_dashboard.urls')),
    path('api/files/', include('apps.file_storage.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug toolbar for development
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
