from django import template
from riskforms.models import Participant


register = template.Library()


@register.filter(name='in_client')
def in_client(appointments, client):
    return appointments.filter(client=client)


@register.filter(name='is_participant')
def is_participant(appointment, client):
    all_parts = Participant.objects.all()
    all_parts = all_parts.filter(client=client)
    for part in all_parts:
        all_apps = part.appointment.all()
        for app in all_apps:
            if app == appointment:
                return True
    return False


@register.filter(name='remaining_forms')
def remaining_forms(appParts, partNum):
    return (appParts-partNum)
