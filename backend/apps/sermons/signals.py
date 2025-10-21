import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Sermon
from .tasks import process_audio_file

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Sermon)
def handle_sermon_save(sender, instance, created, **kwargs):
    """Handle post-save operations for Sermon model."""
    try:
        # If this is a new sermon with an audio file, queue it for processing
        if created and instance.audio_file:
            logger.info(f"New sermon {instance.id} created with audio file, queuing for processing")
            process_audio_file.delay(instance.id)
            
        # If audio file was changed, update metadata
        if not created and instance.audio_file:
            # Check if this is an update with a new file
            try:
                old_instance = Sermon.objects.get(pk=instance.pk)
                if old_instance.audio_file != instance.audio_file:
                    logger.info(f"Audio file changed for sermon {instance.id}, requeuing for processing")
                    process_audio_file.delay(instance.id)
            except Sermon.DoesNotExist:
                pass
                
    except Exception as e:
        logger.error(f"Error in handle_sermon_save for sermon {instance.id}: {str(e)}")
        raise

@receiver(pre_save, sender=Sermon)
def validate_sermon(sender, instance, **kwargs):
    """Pre-save validation for Sermon model."""
    # This will call the clean() method we defined in the model
    instance.clean()
