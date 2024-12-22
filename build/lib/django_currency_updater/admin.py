from django.contrib import admin
from django_currency_updater.models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'rate')
