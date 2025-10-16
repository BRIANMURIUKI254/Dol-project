from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.events.models import Event


class Command(BaseCommand):
    help = 'Synchronizes event_type and upcoming status based on event_date.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting event status synchronization...'))
        
        now = timezone.now()
        updated_count = 0
        dry_run = options['dry_run']

        # Get all events
        events = Event.objects.all()

        for event in events:
            original_event_type = event.event_type
            original_upcoming = event.upcoming

            # Check what the new values should be
            if event.event_date:
                if event.event_date > now:
                    new_event_type = 'upcoming'
                    new_upcoming = True
                else:
                    new_event_type = 'past'
                    new_upcoming = False
            else:
                # Skip events without event_date
                continue

            # Check if update is needed
            if event.event_type != new_event_type or event.upcoming != new_upcoming:
                updated_count += 1
                
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            f"[DRY RUN] Would update event '{event.title}' (ID: {event.id}): "
                            f"event_type '{original_event_type}' → '{new_event_type}', "
                            f"upcoming {original_upcoming} → {new_upcoming}"
                        )
                    )
                else:
                    # Actually update the event
                    event.event_type = new_event_type
                    event.upcoming = new_upcoming
                    event.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated event '{event.title}' (ID: {event.id}): "
                            f"event_type '{original_event_type}' → '{new_event_type}', "
                            f"upcoming {original_upcoming} → {new_upcoming}"
                        )
                    )
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'[DRY RUN] Would update {updated_count} events. Run without --dry-run to apply changes.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Finished event status synchronization. {updated_count} events updated.'
            ))
