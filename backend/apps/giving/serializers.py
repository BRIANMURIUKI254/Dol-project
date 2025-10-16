from rest_framework import serializers
from .models import Partnership, Donation


class PartnershipSerializer(serializers.ModelSerializer):
    """Serializer for Partnership model"""
    class Meta:
        model = Partnership
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'partnership_type',
            'amount',
            'message',
            'status',
            'is_recurring',
            'next_payment_date',
            'last_payment_date',
            'payment_reference',
            'created_at',
            'updated_at'
        ]
        read_only_fields = (
            'id', 'status', 'is_recurring', 'next_payment_date', 
            'last_payment_date', 'payment_reference', 'created_at', 'updated_at'
        )


class DonationSerializer(serializers.ModelSerializer):
    """Serializer for Donation model"""
    class Meta:
        model = Donation
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'amount',
            'message',
            'is_anonymous',
            'payment_reference',
            'payment_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = (
            'id', 'payment_reference', 'payment_status', 'created_at', 'updated_at'
        )


class PaymentInitiationSerializer(serializers.Serializer):
    """Serializer for initiating a payment"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=200)
    callback_url = serializers.URLField(required=False)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value


class PaymentVerificationSerializer(serializers.Serializer):
    """Serializer for verifying a payment"""
    checkout_request_id = serializers.CharField(max_length=100)
    mpesa_receipt_number = serializers.CharField(max_length=100, required=False)
    transaction_date = serializers.CharField(max_length=100, required=False)
    phone_number = serializers.CharField(max_length=20, required=False)
    
    def validate(self, data):
        # Add any custom validation here
        return data
