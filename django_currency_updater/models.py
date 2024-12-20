from django.db import models
from django.apps import apps

def create_currency_model():
    """
    Dynamically create the Currency model.
    """
    class Meta:
        app_label = 'django_currency_updater'
        managed = True

    attrs = {
        'code': models.CharField(max_length=3, unique=True),
        'rate': models.DecimalField(max_digits=10, decimal_places=4),
        '__module__': __name__,
        'Meta': Meta,
    }

    model = type('Currency', (models.Model,), attrs)
    if not apps.is_installed('django_currency_updater'):
        raise RuntimeError("Add 'django_currency_updater' to INSTALLED_APPS.")

    return model

Currency = create_currency_model()
