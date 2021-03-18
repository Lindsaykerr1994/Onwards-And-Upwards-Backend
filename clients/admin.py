from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'abbreviation',
        'email_address',
        'phone_number'
    )

    ordering = ('last_name', 'first_name')


admin.site.register(Client, ClientAdmin)
