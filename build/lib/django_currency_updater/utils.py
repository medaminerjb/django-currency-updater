from django.conf import settings
from django_currency_updater.models import Currency

def set_currency(request, currency_code):
    """
    Set the current currency for the session.
    """
    request.session['currency'] = currency_code

def get_currency(request):
    """
    Get the current currency for the session or default.
    """
    return request.session.get('currency', settings.DEFAULT_CURRENCY)

def get_currency_rate(code):
    """
    Fetch the exchange rate for the given currency code.
    """
    try:
        currency = Currency.objects.get(code=code)
        return currency.rate
    except Currency.DoesNotExist:
        return None
