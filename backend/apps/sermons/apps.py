from django.apps import AppConfig


class SermonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sermons'
    verbose_name = 'Sermon Management'

    def ready(self):
        # Import signals to connect them
        import apps.sermons.signals  # noqa
        
        # Import tasks to ensure they're registered with Celery
        import apps.sermons.tasks  # noqa
