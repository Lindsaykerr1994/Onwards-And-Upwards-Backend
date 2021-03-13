from django import template


register = template.Library()


@register.filter(name='in_client')
def in_client(appointments, client):
    return appointments.filter(client=client)


@register.filter(name='remaining_forms')
def remaining_forms(appParts, partNum):
    return (appParts-partNum)
