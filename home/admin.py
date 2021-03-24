from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'date_created',
        'classification',
        'message',
        'reference',

    )

    ordering = ('date_created', 'classification')


admin.site.register(Notification, NotificationAdmin)
