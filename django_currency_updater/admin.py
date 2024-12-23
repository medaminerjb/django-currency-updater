from django.contrib import admin
from django_currency_updater.models import Currency,SchedulerSettings
from django.core.exceptions import ValidationError

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'rate')

@admin.register(SchedulerSettings)
class SchedulerSettingsAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'hour_of_day', 'day_of_week', 'interval_minutes', 'interval_seconds')
    fieldsets = (
        (None, {
            'fields': ('frequency', 'hour_of_day', 'day_of_week', 'interval_minutes', 'interval_seconds'),
        }),
    )
    def has_add_permission(self, request):
        # Allow only one instance of SchedulerSettings
        if SchedulerSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to enforce single-instance constraint and validate the model.
        """
        # Enforce single instance rule
        if not change and SchedulerSettings.objects.exists():
            raise ValidationError("You can only have one SchedulerSettings instance.")
        
        # Call model's `clean` method for validation
        obj.clean()
        
        # Save the object
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only if a SchedulerSettings instance already exists.
        """
        if SchedulerSettings.objects.exists():
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)