from django.test import TestCase
from unittest.mock import patch
from django_currency_updater.updater import update_currency_rate

class UpdateCurrencyRateTests(TestCase):
    @patch("requests.get")
    def test_update_currency_rate_success(self, mock_get):
        mock_response = {
            "rates": {"USD": 1.0, "EUR": 0.85, "GBP": 0.75},
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        update_currency_rate()

        # Add assertions to verify database updates
        # Example: self.assertTrue(Currency.objects.filter(code="USD").exists())
