
`django-currency-updater` is a reusable Django library that fetches the latest currency exchange rates from an external API and updates them in your database. This library dynamically generates a `Currency` model and provides a simple function to manage currency data.
## Features- 
**Dynamic Model Generation**: 
Automatically creates a `Currency` model to store currency codes and rates.
- **Flexible Configuration**: Easily configure the API URL and list of currencies in your Django settings.
- **Seamless Integration**: Use as a standalone Django app or integrate it into an existing project.
- **Error Handling**: Includes robust error handling for API requests and database operations.
- ## Installation
1. Install the library:```bash pip install django-currency-updater ```
2. Add `django_currency_updater` to your `INSTALLED_APPS` in `settings.py`: ```python INSTALLED_APPS = [ ... 'django_currency_updater', ] ```
3. Apply migrations (if required): ```bash python manage.py migrate ```
## ConfigurationAdd 
the following settings to your Django project’s `settings.py` file:
### Example Configuration
```
python# API URL for fetching currency ratesCURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
# List of currencies to manage
CURRENCIES = [ ("USD", "US Dollar"), ("EUR", "Euro"), ("GBP", "British Pound"),]
```
### Default Configuration

- **CURRENCY_API_URL**: Defaults to `https://api.exchangerate-api.com/v4/latest/USD`.
- **CURRENCIES**: Defaults to an empty list (`[]`).

## Usage
### Updating Currency Rates


Call the `update_currency_rate` function to fetch and update currency rates:

python
`from django_currency_updater.updater import update_currency_rate  # Update currency rates update_currency_rate()`
### Accessing Currency Data

The library dynamically generates a `Currency` model, which you can use to query the database:

python

Copier le code

`from django_currency_updater.models import Currency  # Query all currencies currencies = Currency.objects.all()  # Get a specific currency usd = Currency.objects.get(code="USD") print(f"USD Rate: {usd.rate}")`
## Testing

Run tests using Django’s test framework:

bash

Copier le code

`python manage.py test django_currency_updater`

## Contributing

We welcome contributions! Feel free to submit issues, feature requests, or pull requests on GitHub.

## License

This library is licensed under the MIT License. See the LICENSE file for details.

## Author

Developed by Your Mohamed Lamine Rejeb.

