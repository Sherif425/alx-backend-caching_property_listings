# from django.apps import AppConfig
# import properties.signals

# class PropertiesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'properties'

from django.apps import AppConfig

class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        # Import signals only when apps are ready ✅
        import properties.signals
