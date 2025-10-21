from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SermonViewSet, SermonCategoryViewSet

app_name = 'sermons'

# Router for ViewSets
router = DefaultRouter()
router.register(r'sermons', SermonViewSet, basename='sermon')
router.register(r'categories', SermonCategoryViewSet, basename='sermon-category')

urlpatterns = [
    # Include ViewSet URLs
    path('', include(router.urls)),
]
