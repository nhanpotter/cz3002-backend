from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    name = 'authentication'
    def ready(self):
        from .createGroup import create_group
