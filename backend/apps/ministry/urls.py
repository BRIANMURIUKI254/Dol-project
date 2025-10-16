from django.urls import path
from . import views

app_name = 'ministry'

urlpatterns = [
    # Ministry Information
    path('info/', views.MinistryInfoView.as_view(), name='ministry-info'),
    
    # Carousel Images
    path('carousel/', views.CarouselImageView.as_view(), name='carousel-list'),
    path('carousel/<int:pk>/', views.CarouselImageDetailView.as_view(), name='carousel-detail'),
]
