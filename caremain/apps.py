from django.apps import AppConfig


class CaremainConfig(AppConfig):
    name = 'caremain'

    def ready(self):
        import caremain.signals

    
