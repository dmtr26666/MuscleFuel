from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MuscleFuel.accounts'

    def ready(self):
        import MuscleFuel.accounts.signals
