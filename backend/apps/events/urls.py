from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # List and create events
    path('', views.EventListView.as_view(), name='event-list'),
    
    # Retrieve, update, or delete an event
    path('<uuid:id>/', views.EventDetailView.as_view(), name='event-detail'),
    
    # Featured events
    path('featured/', views.FeaturedEventsView.as_view(), name='featured-events'),
]
