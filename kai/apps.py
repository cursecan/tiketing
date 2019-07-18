from django.apps import AppConfig


class KaiConfig(AppConfig):
    name = 'kai'

    def ready(self):
        from . import signals
