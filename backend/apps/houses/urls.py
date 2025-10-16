from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    # List and create houses
    path('', views.HouseListView.as_view(), name='house-list'),
    
    # Retrieve, update, or delete a house
    path('<int:id>/', views.HouseDetailView.as_view(), name='house-detail'),
]
