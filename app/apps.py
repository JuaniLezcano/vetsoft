from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Configuración de la aplicación.

    Esta clase define la configuración de la aplicación, como la configuración de la base de datos,
    las aplicaciones instaladas, las rutas de URL, etc.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
