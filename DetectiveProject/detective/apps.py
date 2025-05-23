from django.apps import AppConfig


class DetectiveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "detective"

    def ready(self):
        # Importera signalerna så att de registreras
        import detective.signals

from django.apps import AppConfig

