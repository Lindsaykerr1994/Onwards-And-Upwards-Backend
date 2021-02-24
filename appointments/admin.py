from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment_number',
        'created_date',
        'client',
        'activity',
        'course'
    )

    ordering = ('appointment_number',)


admin.site.register(Appointment, AppointmentAdmin)
