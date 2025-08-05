from django.apps import AppConfig

class ForexAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forex_app'

    # def ready(self):
    #     from .services.scheduler import start_scheduler
    #     start_scheduler()
