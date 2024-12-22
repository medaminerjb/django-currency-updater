from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

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

