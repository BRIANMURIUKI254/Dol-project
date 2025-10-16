import time
from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Partnership, Donation
from .serializers import (
    PartnershipSerializer, 
    DonationSerializer,
    PaymentInitiationSerializer,
    PaymentVerificationSerializer
)
from apps.core.permissions import IsAdminOrReadOnly


class PartnershipListView(generics.ListCreateAPIView):
    """View to list and create partnerships"""
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'partnership_type', 'is_recurring']
    
    def get_queryset(self):
        # Non-admin users can only see their own partnerships
        if not self.request.user.is_staff:
            return Partnership.objects.filter(email=self.request.user.email)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        # Set the user's email if authenticated
        if self.request.user.is_authenticated:
            serializer.save(email=self.request.user.email)
        else:
            serializer.save()


class PartnershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a partnership"""
    queryset = Partnership.objects.all()
    serializer_class = PartnershipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Non-admin users can only see their own partnerships
        if not self.request.user.is_staff:
            return Partnership.objects.filter(email=self.request.user.email)
        return super().get_queryset()


class DonationListView(generics.ListCreateAPIView):
    """View to list and create donations"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'is_anonymous']
    
    def get_queryset(self):
        # Non-admin users can only see their own donations
        if not self.request.user.is_staff:
            return Donation.objects.filter(email=self.request.user.email)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        # Set the user's email if authenticated
        if self.request.user.is_authenticated:
            serializer.save(email=self.request.user.email)
        else:
            serializer.save()


class DonationDetailView(generics.RetrieveAPIView):
    """View to retrieve a donation"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Non-admin users can only see their own donations
        if not self.request.user.is_staff:
            return Donation.objects.filter(email=self.request.user.email)
        return super().get_queryset()


class PaymentResponseSerializer(serializers.Serializer):
    """Serializer for payment response"""
    checkout_request_id = serializers.CharField()
    merchant_request_id = serializers.CharField()
    response_code = serializers.CharField()
    response_description = serializers.CharField()
    customer_message = serializers.CharField()


class InitiatePaymentView(APIView):
    """View to initiate a payment"""
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentInitiationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Here you would typically integrate with a payment gateway like M-Pesa
            # This is a simplified example
            payment_data = {
                'checkout_request_id': f"DOL_{int(time.time())}",
                'merchant_request_id': f"DOL_{int(time.time())}",
                'response_code': '0',
                'response_description': 'Success. Request accepted for processing',
                'customer_message': 'Please complete the payment on your phone.'
            }
            response_serializer = PaymentResponseSerializer(data=payment_data)
            response_serializer.is_valid(raise_exception=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCallbackResponseSerializer(serializers.Serializer):
    """Serializer for payment callback response"""
    ResultCode = serializers.IntegerField()
    ResultDesc = serializers.CharField()


class PaymentCallbackView(APIView):
    """View to handle payment callbacks from payment gateway"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        # This is where you would process the payment callback
        # and update the relevant models (Partnership or Donation)
        response_data = {
            'ResultCode': 0,
            'ResultDesc': 'The service was accepted successfully'
        }
        serializer = PaymentCallbackResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
