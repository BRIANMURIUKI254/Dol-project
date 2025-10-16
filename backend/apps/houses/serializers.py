from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    """Serializer for House model"""
    meeting_schedule = serializers.CharField(
        read_only=True,
        help_text="Formatted meeting schedule with day and time range"
    )
    
    class Meta:
        model = House
        fields = [
            'id',
            'name',
            'location',
            'meeting_day',
            'start_time',
            'end_time',
            'meeting_schedule',
            'description',
            'is_active',
            'order',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'start_time': {'format': '%I:%M %p'},
            'end_time': {'format': '%I:%M %p'},
        }
