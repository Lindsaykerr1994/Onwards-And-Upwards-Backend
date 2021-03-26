from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Notification


def notifications_contents(request):
    notifications = Notification.objects.all()
    unread = notifications.filter(read=False)
    notes_count = len(unread)

    context = {
        'notes_count': notes_count,
        'notifications': notifications
    }
    return context
