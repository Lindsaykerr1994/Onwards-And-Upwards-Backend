from django.contrib import admin
from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
    )

    ordering = ('last_name', 'first_name')


admin.site.register(Participant, ParticipantAdmin)
