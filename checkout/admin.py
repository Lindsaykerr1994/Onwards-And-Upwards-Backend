from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'receipt_no',
        'date',
        'full_name',
    )

    ordering = ('-date', 'receipt_no', 'full_name')


admin.site.register(Payment, PaymentAdmin)
