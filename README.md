# Django Currency Updater

`django-currency-updater` is a reusable Django library that fetches the latest currency exchange rates from an external API and updates them in your database. This library dynamically generates a `Currency` model and provides simple functions to manage currency data and schedule updates.

---

## Features

- **Dynamic Model Generation**: Automatically creates a `Currency` model to store currency codes and rates.
- **Flexible Configuration**: Easily configure the API URL and list of currencies in your Django settings.
- **Seamless Integration**: Use as a standalone Django app or integrate it into an existing project.
- **Error Handling**: Includes robust error handling for API requests and database operations.
- **Task Scheduling**: Schedule periodic updates for currency rates using a scheduler.
- **Currency Preloading**: Load predefined currency data into the database.
- **Currency Conversion in Templates**: Use the {% currency %} template tag to convert prices between currencies directly in your Django templates.

---

## Installation

1. Install the library:
   ```bash
   pip install django-currency-updater
   ```

2. Add `django_currency_updater` to your `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'django_currency_updater',
   ]
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

---

## Configuration

Add the following settings to your Django project’s `settings.py` file:

### Example Configuration
```python
# API URL for fetching currency rates
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# List of currencies to manage
CURRENCIES = [
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("GBP", "British Pound")
    ...
]

# Scheduler settings
CURRENCY_UPDATE_SCHEDULE = {
    "frequency": "daily",  # Options: 'hourly', 'daily', 'weekly', 'custom'
    "hour_of_day": 3,       # For 'daily' and 'weekly'
    "day_of_week": None,    # For 'weekly' (0=Monday, 6=Sunday)
    "interval_minutes": None,  # For 'custom'
    "interval_seconds": None,  # For 'custom'
}
```

### Default Configuration
- `CURRENCY_API_URL`: Defaults to `https://api.exchangerate-api.com/v4/latest/USD`.
- `CURRENCIES`: Defaults to an empty list (`[]`).
- `CURRENCY_UPDATE_SCHEDULE`: Defaults to hourly updates.

---

## Usage

### Updating Currency Rates
Call the `update_currency_rate` function to fetch and update currency rates:

```python
from django_currency_updater.updater import update_currency_rate

# Update currency rates
update_currency_rate()
```

### Scheduling Currency Updates
The library integrates with Django’s admin and supports scheduling periodic updates via the `SchedulerSettings` model:

1. Set the scheduling parameters in `CURRENCY_UPDATE_SCHEDULE`.
2. Use the admin interface to verify or adjust scheduling settings.
3. Ensure your task runner (e.g., Celery or APScheduler) is running to execute the scheduled updates.

### Preloading Currency Data
Use the `load_currencies` command to preload currency data into the database:

```bash
python manage.py load_currencies
```

### Accessing Currency Data
The library dynamically generates a `Currency` model, which you can use to query the database:

```python
from django_currency_updater.models import Currency

# Query all currencies
currencies = Currency.objects.all()

# Get a specific currency
usd = Currency.objects.get(code="USD")
print(f"USD Rate: {usd.rate}")
```
## Template Tags
### Currency Conversion in Templates
The library provides a template tag to convert currencies directly within your Django templates.

#### Usage Example:
In your template, load the currency_tags and use the {% currency %} tag to convert an amount from one currency to another.
```html
{% load currency_tags %}

<p>Price in EUR: {% currency 100 %} </p>
```
#### Arguments:
- **amount**: The amount to be converted
- **from_currency**: The currency code to convert from (default: "USD").
- **to_currency**: The currency code to convert to (default: "EUR").
---

## Testing

Run tests using Django’s test framework:

```bash
python manage.py test django_currency_updater
```

---

## Contributing

We welcome contributions! Feel free to submit issues, feature requests, or pull requests on GitHub.

---

## License

This library is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Developed by Mohamed Lamine Rejeb.

