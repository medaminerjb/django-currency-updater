from django.conf import settings

# Default API URL
DEFAULT_CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Default list of currencies
DEFAULT_CURRENCIES = []

# Settings with fallbacks
CURRENCY_API_URL = getattr(settings, "CURRENCY_API_URL", DEFAULT_CURRENCY_API_URL)
CURRENCIES = getattr(settings, "CURRENCIES", DEFAULT_CURRENCIES)
