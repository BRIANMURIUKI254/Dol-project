from django.urls import path
from . import views

app_name = 'giving'

urlpatterns = [
    # Partnerships
    path('partnerships/', views.PartnershipListView.as_view(), name='partnership-list'),
    path('partnerships/<int:pk>/', views.PartnershipDetailView.as_view(), name='partnership-detail'),
    
    # Donations
    path('donations/', views.DonationListView.as_view(), name='donation-list'),
    path('donations/<int:pk>/', views.DonationDetailView.as_view(), name='donation-detail'),
    
    # Payment processing
    path('payments/initiate/', views.InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/callback/', views.PaymentCallbackView.as_view(), name='payment-callback'),
]
