from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    
    # Note: signal NOT work without this code :
    def ready(self):
        import user.signals