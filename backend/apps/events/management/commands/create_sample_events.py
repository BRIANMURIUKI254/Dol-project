from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.events.models import Event, EventCategory


class Command(BaseCommand):
    help = 'Create sample events for testing'

    def handle(self, *args, **options):
        # Create event categories
        worship_category, created = EventCategory.objects.get_or_create(
            name='Worship Experience',
            defaults={'description': 'Worship and praise events'}
        )
        
        conference_category, created = EventCategory.objects.get_or_create(
            name='Conference',
            defaults={'description': 'Conferences and seminars'}
        )
        
        concert_category, created = EventCategory.objects.get_or_create(
            name='Concert',
            defaults={'description': 'Musical concerts and performances'}
        )

        # Sample events data
        events_data = [
            {
                'title': 'Desire Concert',
                'description': 'An amazing worship concert featuring contemporary Christian music and powerful worship experiences.',
                'event_type': 'past',
                'category': concert_category,
                'event_date': timezone.make_aware(datetime(2022, 6, 15, 19, 0)),
                'end_date': timezone.make_aware(datetime(2022, 6, 15, 22, 0)),
                'location': 'Main Auditorium, Kenyatta University',
                'image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop&crop=center',
                'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'featured': True,
            },
            {
                'title': 'Photizo Worship Experience',
                'description': 'A transformative worship experience that brings light and revelation through powerful worship and teaching.',
                'event_type': 'past',
                'category': worship_category,
                'event_date': timezone.make_aware(datetime(2023, 3, 20, 18, 0)),
                'end_date': timezone.make_aware(datetime(2023, 3, 20, 21, 0)),
                'location': 'Worship Center, Main Campus',
                'image': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&h=600&fit=crop&crop=center',
                'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'featured': True,
            },
            {
                'title': 'Desire Kesha',
                'description': 'A powerful worship night featuring contemporary worship music and spiritual encounters.',
                'event_type': 'past',
                'category': worship_category,
                'event_date': timezone.make_aware(datetime(2023, 8, 12, 19, 30)),
                'end_date': timezone.make_aware(datetime(2023, 8, 12, 22, 30)),
                'location': 'Outdoor Amphitheater, University Grounds',
                'image': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&h=600&fit=crop&crop=center',
                'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'featured': False,
            },
            {
                'title': 'King Of My Heart',
                'description': 'A special worship event celebrating the sovereignty and love of our King, featuring powerful worship and testimonies.',
                'event_type': 'past',
                'category': worship_category,
                'event_date': timezone.make_aware(datetime(2024, 2, 14, 18, 0)),
                'end_date': timezone.make_aware(datetime(2024, 2, 14, 21, 0)),
                'location': 'Main Auditorium, Kenyatta University',
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop&crop=center',
                'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'featured': True,
            },
            {
                'title': 'Sunday Service',
                'description': 'Join us for our weekly Sunday service as we worship and learn together in the presence of God.',
                'event_type': 'upcoming',
                'category': worship_category,
                'event_date': timezone.now() + timedelta(days=3),
                'end_date': timezone.now() + timedelta(days=3, hours=2),
                'location': 'Main Auditorium, Kenyatta University',
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop&crop=center',
                'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'featured': True,
            },
            {
                'title': 'Prayer Meeting',
                'description': 'Corporate prayer and intercession for the nation and our community. Join us as we seek God together.',
                'event_type': 'upcoming',
                'category': worship_category,
                'event_date': timezone.now() + timedelta(days=7),
                'end_date': timezone.now() + timedelta(days=7, hours=2),
                'location': 'Prayer Room, Main Campus',
                'image': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&h=600&fit=crop&crop=center',
                'featured': False,
            },
        ]

        # Create events
        created_count = 0
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                event_date=event_data['event_date'],
                defaults=event_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created event: {event.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Event already exists: {event.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new events')
        )
