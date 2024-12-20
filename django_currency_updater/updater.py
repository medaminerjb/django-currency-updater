import requests
import logging
from django.conf import settings
from .models import create_currency_model

logger = logging.getLogger(__name__)

Currency = create_currency_model()

def update_currency_rate():
    """
    Updates the currency exchange rates in the database.

    Fetches rates from an external API and updates the database.
    """
    url = getattr(settings, "CURRENCY_API_URL", "https://api.exchangerate-api.com/v4/latest/USD")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching currency rates: {e}")
        return

    data = response.json()
    rates = data.get("rates", {})
    if not rates:
        logger.error("Invalid API response: 'rates' key missing or empty.")
        return

    currencies_to_update = getattr(settings, "CURRENCIES", [])
    if not currencies_to_update:
        logger.warning("No currencies specified in settings.")
        return

    currency_codes = [currency[0] for currency in currencies_to_update]

    for currency_code, rate in rates.items():
        if currency_code in currency_codes:
            try:
                currency, created = Currency.objects.update_or_create(
                    code=currency_code,
                    defaults={'rate': rate},
                )
                if created:
                    logger.info(f"Created new currency rate for {currency_code}")
                else:
                    logger.info(f"Updated currency rate for {currency_code}")
            except Exception as e:
                logger.error(f"Error updating currency {currency_code}: {e}")
