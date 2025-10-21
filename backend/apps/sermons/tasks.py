import logging
from celery import shared_task
from django.core.files.storage import default_storage
from django.conf import settings
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from .models import Sermon

logger = logging.getLogger(__name__)

def get_audio_duration(file_path):
    """Get duration of audio file in seconds using mutagen."""
    try:
        audio = File(file_path)
        if audio is None:
            return 0
            
        # Get duration based on file type
        if hasattr(audio.info, 'length'):
            return int(audio.info.length)
        elif hasattr(audio.info, 'length_seconds'):
            return int(audio.info.length_seconds)
        return 0
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return 0

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_audio_file(self, sermon_id):
    """Process an uploaded audio file to extract metadata."""
    try:
        sermon = Sermon.objects.get(id=sermon_id)
        
        if not sermon.audio_file:
            logger.warning(f"No audio file found for sermon {sermon_id}")
            return
            
        # Update status to processing
        sermon.processing_status = 'processing'
        sermon.save(update_fields=['processing_status', 'updated_at'])
        
        try:
            # Get file path from Cloudinary
            file_path = sermon.audio_file.path
            
            # Get duration using mutagen
            duration = get_audio_duration(file_path)
            
            # Update sermon with metadata
            sermon.duration = duration
            sermon.processing_status = 'completed'
            sermon.save(update_fields=['duration', 'processing_status', 'updated_at'])
            
            logger.info(f"Successfully processed audio for sermon {sermon_id}")
            
        except Exception as e:
            error_msg = f"Error processing audio: {str(e)}"
            logger.error(f"{error_msg} for sermon {sermon_id}")
            sermon.processing_status = 'failed'
            sermon.processing_errors = error_msg
            sermon.save(update_fields=['processing_status', 'processing_errors', 'updated_at'])
            raise  # Re-raise to trigger Celery retry
            
    except Sermon.DoesNotExist:
        logger.error(f"Sermon {sermon_id} not found")
    except Exception as e:
        logger.error(f"Unexpected error processing sermon {sermon_id}: {str(e)}")
        # If we've retried enough, mark as failed
        if self.request.retries >= self.max_retries:
            sermon.processing_status = 'failed'
            sermon.processing_errors = f"Max retries reached: {str(e)}"
            sermon.save(update_fields=['processing_status', 'processing_errors', 'updated_at'])
        raise self.retry(exc=e)

@shared_task
generate_audio_waveform(sermon_id):
    ""
    Generate a waveform representation of the audio file.
    This is an optional task that can be called after process_audio_file.
    """
    try:
        sermon = Sermon.objects.get(id=sermon_id)
        if not sermon.audio_file:
            return
            
        # This is a placeholder - you would typically use a library like librosa or pydub
        # to generate waveform data and store it as JSON or an image
        logger.info(f"Generating waveform for sermon {sermon_id}")
        
    except Exception as e:
        logger.error(f"Error generating waveform: {str(e)}")
        raise
