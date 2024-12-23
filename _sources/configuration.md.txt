Configuration
=============

You can configure the `django-currency-updater` library in your Django project's `settings.py` file.

## Example Configuration
```python

# API URL for fetching currency rates
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
# List of currencies to manage
CURRENCIES = [
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("GBP", "British Pound")
    # Add more currencies here
]
## Auto scheduler enabled
ENABLE_SCHEDULER = True
# Scheduler settings
```
update scheduler settings model 
