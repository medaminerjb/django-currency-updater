from django.core.management.base import BaseCommand
import requests
import logging
import json
import os  # Import os for file path handling
from django.conf import settings
from django_currency_updater.models import create_currency_model

# Initialize logger
logger = logging.getLogger(__name__)

# Dynamically create Currency model
Currency = create_currency_model()
symbols_data = {
    "USD": "$",
    "CAD": "CA$",
    "EUR": "€",
    "AED": "AED",
    "AFN": "Af",
    "ALL": "ALL",
    "AMD": "AMD",
    "ARS": "AR$",
    "AUD": "AU$",
    "AZN": "man.",
    "BAM": "KM",
    "BDT": "Tk",
    "BGN": "BGN",
    "BHD": "BD",
    "BIF": "FBu",
    "BND": "BN$",
    "BOB": "Bs",
    "BRL": "R$",
    "BWP": "BWP",
    "BYN": "Br",
    "BZD": "BZ$",
    "CDF": "CDF",
    "CHF": "CHF",
    "CLP": "CL$",
    "CNY": "CN¥",
    "COP": "CO$",
    "CRC": "₡",
    "CVE": "CV$",
    "CZK": "Kč",
    "DJF": "Fdj",
    "DKK": "Dkr",
    "DOP": "RD$",
    "DZD": "DA",
    "EEK": "Ekr",
    "EGP": "EGP",
    "ERN": "Nfk",
    "ETB": "Br",
    "GBP": "£",
    "GEL": "GEL",
    "GHS": "GH₵",
    "GNF": "FG",
    "GTQ": "GTQ",
    "HKD": "HK$",
    "HNL": "HNL",
    "HRK": "kn",
    "HUF": "Ft",
    "IDR": "Rp",
    "ILS": "₪",
    "INR": "₹",
    "IQD": "IQD",
    "IRR": "IRR",
    "ISK": "Ikr",
    "JMD": "J$",
    "JOD": "JD",
    "JPY": "¥",
    "KES": "Ksh",
    "KHR": "KHR",
    "KMF": "CF",
    "KRW": "₩",
    "KWD": "KD",
    "KZT": "KZT",
    "LBP": "L.L.",
    "LKR": "SLRs",
    "LTL": "Lt",
    "LVL": "Ls",
    "LYD": "LD",
    "MAD": "MAD",
    "MDL": "MDL",
    "MGA": "MGA",
    "MKD": "MKD",
    "MMK": "MMK",
    "MOP": "MOP$",
    "MUR": "MURs",
    "MXN": "MX$",
    "MYR": "RM",
    "MZN": "MTn",
    "NAD": "N$",
    "NGN": "₦",
    "NIO": "C$",
    "NOK": "Nkr",
    "NPR": "NPRs",
    "NZD": "NZ$",
    "OMR": "OMR",
    "PAB": "B/.",
    "PEN": "S/.",
    "PHP": "₱",
    "PKR": "PKRs",
    "PLN": "zł",
    "PYG": "₲",
    "QAR": "QR",
    "RON": "RON",
    "RSD": "din.",
    "RUB": "RUB",
    "RWF": "RWF",
    "SAR": "SR",
    "SDG": "SDG",
    "SEK": "Skr",
    "SGD": "S$",
    "SOS": "Ssh",
    "SYP": "SY£",
    "THB": "฿",
    "TND": "DT",
    "TOP": "T$",
    "TRY": "TL",
    "TTD": "TT$",
    "TWD": "NT$",
    "TZS": "TSh",
    "UAH": "₴",
    "UGX": "USh",
    "UYU": "$U",
    "UZS": "UZS",
    "VEF": "Bs.F.",
    "VND": "₫",
    "XAF": "FCFA",
    "XOF": "CFA",
    "YER": "YR",
    "ZAR": "R",
    "ZMK": "ZK",
    "ZWL": "ZWL$"
    }
class Command(BaseCommand):
    help = "Fetch and update currency rates from an external API"

    def handle(self, *args, **options):
        """
        Handle the command to fetch and update currency rates.
        """
        self.stdout.write("Starting currency rate update...\n")
        self.update_currency_rate()

    def load_symbols(self):
        """
        Load symbols from the symbols.json file.
        """
        # Assuming symbols.json is located inside a data folder within the app
        symbols_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data', 'symbols.json'
    )
        
        # Check if the symbols.json exists
        if not os.path.exists(symbols_file):
            logger.warning("symbols.json file not found!")
            self.stdout.write(self.style.WARNING('symbols.json file not found!'))
            return {}

        # Load the symbols from the file
        with open(symbols_file, 'r') as file:
            symbols_data = json.load(file)

        return symbols_data
    def update_currency_rate(self):
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
            self.stdout.write(self.style.ERROR(f"Error fetching currency rates: {e}"))
            return

        data = response.json()
        rates = data.get("rates", {})
        if not rates:
            logger.error("Invalid API response: 'rates' key missing or empty.")
            self.stdout.write(self.style.ERROR("Invalid API response: 'rates' key missing or empty."))
            return

        currencies_to_update = getattr(settings, "CURRENCIES", [])
        if not currencies_to_update:
            logger.warning("No currencies specified in settings.")
            self.stdout.write(self.style.WARNING("No currencies specified in settings."))
            return

        currency_codes = [currency[0] for currency in currencies_to_update]

        # Load symbols from symbols.json file
        symbols = symbols_data

        for currency_code, rate in rates.items():
            if currency_code in currency_codes:
                try:
                    # Fetch the symbol from the symbols data
                    symbol = symbols.get(currency_code, "")
                    
                    # Update or create the currency with the symbol
                    currency, created = Currency.objects.update_or_create(
                        code=currency_code,
                        defaults={'rate': rate, 'symbol': symbol},
                    )

                    if created:
                        logger.info(f"Created new currency rate for {currency_code} with symbol {symbol}")
                        self.stdout.write(self.style.SUCCESS(f"Created new currency rate for {currency_code}"))
                    else:
                        logger.info(f"Updated currency rate for {currency_code} with symbol {symbol}")
                        self.stdout.write(self.style.SUCCESS(f"Updated currency rate for {currency_code}"))
                except Exception as e:
                    logger.error(f"Error updating currency {currency_code}: {e}")
                    self.stdout.write(self.style.ERROR(f"Error updating currency {currency_code}: {e}"))
