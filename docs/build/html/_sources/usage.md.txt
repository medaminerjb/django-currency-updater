Usage
============

## Updating Currency Rates

To fetch and update currency rates, you can call the `update_currency_rate` function. Here's an example:

```python
from django_currency_updater.updater import update_currency_rate
```

## Update currency rates
```python
update_currency_rate()
```
## Preloading Currency Data
Use the load_currencies command to preload currency data into the database:

```bash
python manage.py load_currencies
```
## Currency Conversion in Templates
The library provides a template tag to convert currencies directly within your Django templates.

### Usage Example:
In your template, load the currency_tags and use the `{% currency amount %}` tag to convert an amount from one currency to another.
```html
{% load currency_tags %}
```