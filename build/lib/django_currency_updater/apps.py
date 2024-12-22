from django.apps import AppConfig
from django.core.management import call_command
class DjangoCurrencyUpdaterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_currency_updater"
    verbose_name = "Django Currency Updater"
    def ready(self):
        # Run migrations only in development mode
        from django.conf import settings
        if settings.DEBUG:
            try:
                call_command('makemigrations', 'django_currency_updater', interactive=False)
                call_command('migrate', interactive=False)
            except Exception as e:
                print(f"Migration error: {e}")