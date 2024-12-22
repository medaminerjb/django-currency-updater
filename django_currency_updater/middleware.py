# django_currency_updater/middleware.py

from django.conf import settings
from django_currency_updater.models import Currency

class CurrencyMiddleware:
    """
    Middleware to handle the setting of currency based on session or default settings.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the currency code from the session, or fall back to the default currency
        currency_code = request.session.get('currency_code', settings.DEFAULT_CURRENCY)

        try:
            # Get the currency object based on the currency code
            currency = Currency.objects.get(code=currency_code)

            # Attach currency symbol and rate to the request
            request.currency_symbol = currency.symbol
            request.currency_rate = currency.rate
        except Currency.DoesNotExist:
            # If the currency doesn't exist, use the default
            request.currency_symbol = settings.DEFAULT_CURRENCY_SYMBOL
            request.currency_rate = 1  # Default rate, or you can handle it differently

        # Continue processing the request
        response = self.get_response(request)

        return response
