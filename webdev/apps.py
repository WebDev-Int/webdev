from django.apps import AppConfig


class WebdevConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webdev'


    def ready(self):
        import webdev.signals
        