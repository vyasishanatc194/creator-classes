from django.apps import AppConfig


class CreatorConfig(AppConfig):
    name = 'creator'

    def ready(self):
        from creator import signals
