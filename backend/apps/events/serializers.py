from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    is_upcoming = serializers.BooleanField(
        read_only=True,
        help_text="Indicates if the event is upcoming"
    )
    duration = serializers.DurationField(
        read_only=True,
        help_text="Duration of the event"
    )
    
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'event_type',
            'category',
            'event_date',
            'end_date',
            'location',
            'image',
            'youtube_link',
            'featured',
            'upcoming',
            'is_upcoming',
            'duration',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'event_date': {'format': '%Y-%m-%d %H:%M'},
            'end_date': {'format': '%Y-%m-%d %H:%M'},
        }
