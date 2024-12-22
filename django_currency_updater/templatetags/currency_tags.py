from django import template
from django_currency_updater.models import Currency

register = template.Library()

@register.simple_tag
def get_currency_rate(code):
    """
    Fetch the exchange rate for a given currency code.
    Usage: {% get_currency_rate "USD" %}
    """
    try:
        currency = Currency.objects.get(code=code)
        return currency.rate
    except Currency.DoesNotExist:
        return "N/A"

@register.filter
def format_currency(value, code):
    """
    Format a value with the currency symbol.
    Usage: {{ 1234.56|format_currency:"USD" }}
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
    }
    symbol = symbols.get(code, "")
    return f"{symbol}{value:,.2f}"

@register.simple_tag(takes_context=True)
def currency(context, value):
    """
    Formats a value using the currency stored in the session or defaults to 'USD'.
    Example:
        {% currency 100 %}
    """
    request = context.get('request')
    code = request.session.get('currency', 'USD') if request else 'USD'
    try:
        currency = Currency.objects.get(code=code)
        rate = Currency.objects.get(code=code).rate
        value *= rate
        return f"{currency.symbol or ''}{value:.2f}"
    except Currency.DoesNotExist:
        return value

