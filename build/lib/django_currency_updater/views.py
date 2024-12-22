from django.shortcuts import redirect
from django_currency_updater.models import Currency

def switch_currency(request, currency_code):
    """
    Switch the currency to the provided currency code and store it in the session.
    """
    try:
        # Try to find the currency by its code
        currency = Currency.objects.get(code=currency_code)
        
        # Save the selected currency to the session
        request.session['currency'] = currency_code

        # Redirect to the previous page or any page (you can customize this)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Currency.DoesNotExist:
        # Handle the case where the currency does not exist
        return redirect('currency_switch_error')  # Or any other error page URL
