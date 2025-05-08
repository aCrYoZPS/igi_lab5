from django.apps import AppConfig


class CleaningServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cleaning_service'

    def ready(self):
        import cleaning_service.signals
