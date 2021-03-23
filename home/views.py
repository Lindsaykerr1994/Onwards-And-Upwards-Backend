from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .models import Notification
from django.contrib.auth.models import User


@login_required
def index(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, You don't have permission to do that.")
        return redirect(reverse('home'))
    profile = get_object_or_404(User, id=request.user.id)
    appointments = Appointment.objects.all()
    context = {
        'profile': profile,
        'appointments': appointments
    }
    return render(request, 'home/index.html', context)


@login_required
def notifications(request):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))
    notifications = Notification.objects.all()
    context = {
        'notifications': notifications
    }
    return render(request, 'home/notifications.html', context)


@login_required
def view_notification(request, note_id):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))
    context = {

    }
    return render(request, 'home/view_notification.html', context)
