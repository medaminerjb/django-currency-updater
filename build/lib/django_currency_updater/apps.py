from django.apps import AppConfig
from django.core.management import call_command
import os

class DjangoCurrencyUpdaterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_currency_updater"
    verbose_name = "Django Currency Updater"

    def ready(self):
        from django.conf import settings

        # Scheduler logic
        if getattr(settings, "ENABLE_SCHEDULER", False):
            try:
                # Avoid multiple scheduler startups in multi-threaded environments
                if os.environ.get("RUN_MAIN", None) == "true":  
                    from .scheduler import start_scheduler
                    start_scheduler()
            except Exception as e:
                print(f"Scheduler error: {e}")
