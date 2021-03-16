from django.contrib import admin
from .models import Participant, RAForm


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
    )

    ordering = ('last_name', 'first_name')


class RAFormAdmin(admin.ModelAdmin):
    list_display = (
        'form_number',
        'date_created'
    )

    ordering = ('form_number', 'date_created')


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(RAForm, RAFormAdmin)
