from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Notification


def notifications_contents(request):
    notifications = Notification.objects.all()
    notes_count = len(notifications)

    context = {
        'notes_count': notes_count,
        'notifications': notifications
    }
    return context
