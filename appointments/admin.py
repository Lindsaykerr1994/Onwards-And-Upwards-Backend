from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment_number',
        'appointment_date',
        'created_date',
        'client',
        'activity',
        'course'
    )

    ordering = ('appointment_number', 'appointment_date', 'created_date')


admin.site.register(Appointment, AppointmentAdmin)
