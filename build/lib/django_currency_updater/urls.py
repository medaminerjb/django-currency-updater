from django.urls import path
from django_currency_updater.views import switch_currency

urlpatterns = [
    path('currency/<str:currency_code>/', switch_currency, name='switch_currency'),
]
