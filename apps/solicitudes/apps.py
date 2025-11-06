from django.apps import AppConfig


class SolicitudesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.solicitudes'

    def ready(self):
        import apps.solicitudes.signals
