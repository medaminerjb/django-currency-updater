from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError

def create_currency_model():
    """
    Dynamically create the Currency model for storing currency data.
    Ensures the model is managed by Django and scoped to the app 'django_currency_updater'.
    """
    # Check if the app is installed
    if not apps.is_installed('django_currency_updater'):
        raise ImproperlyConfigured(
            "The app 'django_currency_updater' must be added to INSTALLED_APPS in settings.py."
        )

    # Define the Meta class dynamically
    class Meta:
        app_label = 'django_currency_updater'
        managed = True
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    # Attributes for the Currency model
    attrs = {
        'code': models.CharField(max_length=3, unique=True, verbose_name="Currency Code"),
        'rate': models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Exchange Rate"),
        'symbol': models.CharField(max_length=3, null=True,blank=True, verbose_name="Currency Symbol"),
        '__module__': __name__,
        'Meta': Meta,
    }

    # Create the model class dynamically
    return type('Currency', (models.Model,), attrs)

# Create the Currency model
Currency = create_currency_model()


class SchedulerSettings(models.Model):
    FREQUENCY_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom Interval'),
    ]

    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='hourly',
        help_text="Select the frequency for the updates.",
    )
    hour_of_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="For daily/weekly updates: Choose the hour (0-23).",
    )
    day_of_week = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="For weekly updates: Choose the day (0=Monday, 6=Sunday).",
    )
    interval_minutes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="For custom interval updates: Specify minutes (1-59).",
    )
    interval_seconds = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="For custom interval updates: Specify seconds (1-59).",
    )

    def __str__(self):
        if self.frequency == 'custom':
            return f"Custom updates every {self.interval_minutes or 0} minutes and {self.interval_seconds or 0} seconds"
        elif self.frequency == 'hourly':
            return "Hourly updates"
        elif self.frequency == 'daily':
            return f"Daily updates at {self.hour_of_day}:00"
        elif self.frequency == 'weekly':
            return f"Weekly updates on day {self.day_of_week} at {self.hour_of_day}:00"

    def clean(self):
        """
        Validates the fields based on the selected frequency.
        """
        # Reset unnecessary fields
        if self.frequency == 'hourly':
            self.hour_of_day = None
            self.day_of_week = None
            self.interval_minutes = None
            self.interval_seconds = None

        elif self.frequency == 'daily':
            if self.hour_of_day is None:
                raise ValidationError("Daily updates require 'hour_of_day'.")
            self.day_of_week = None
            self.interval_minutes = None
            self.interval_seconds = None

        elif self.frequency == 'weekly':
            if self.hour_of_day is None or self.day_of_week is None:
                raise ValidationError("Weekly updates require 'hour_of_day' and 'day_of_week'.")
            self.interval_minutes = None
            self.interval_seconds = None

        elif self.frequency == 'custom':
            if (self.interval_minutes is None or self.interval_minutes <= 0) and (
                self.interval_seconds is None or self.interval_seconds <= 0
            ):
                raise ValidationError("Custom interval updates require 'interval_minutes' or 'interval_seconds'.")
            self.hour_of_day = None
            self.day_of_week = None

    def get_schedule_params(self):
        """
        Returns the appropriate schedule parameters for Celery or other schedulers.
        """
        if self.frequency == 'hourly':
            return {"trigger": "interval", "hours": 1}
        elif self.frequency == 'daily':
            return {"trigger": "cron", "hour": self.hour_of_day}
        elif self.frequency == 'weekly':
            return {
                "trigger": "cron",
                "hour": self.hour_of_day,
                "day_of_week": self.day_of_week,
            }
        elif self.frequency == 'custom':
            return {
                "trigger": "interval",
                "minutes": self.interval_minutes or 0,
                "seconds": self.interval_seconds or 0,
            }

