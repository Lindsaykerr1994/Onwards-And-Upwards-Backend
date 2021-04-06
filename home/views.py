from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import datetime
from appointments.models import Appointment
from checkout.models import Payment
from .models import Notification
from django.contrib.auth.models import User


@login_required
def index(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, You don't have permission to do that.")
        return redirect(reverse('home'))
    appointments = Appointment.objects.all()
    profile = get_object_or_404(User, id=request.user.id)
    appointments = appointments.order_by('-appointment_date')
    today = datetime.date.today()
    up_apps = []
    for app in appointments:
        if app.appointment_date >= today:
            up_apps.append(app)
    context = {
        'profile': profile,
        'appointments': up_apps,
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
    notification = Notification.objects.get(pk=note_id)
    appointment = None
    payment = None
    participant = None
    if notification.classification == "PAY":
        appointment = notification.appointment
        payment = notification.payment
    if notification.classification == "PAR":
        participant = notification.participant
        appointment = notification.appointment
    if not notification.read:
        notification.read = True
        notification.save(update_fields=['read'])
    context = {
        'notification': notification,
        'appointment': appointment,
        'payment': payment,
        'participant': participant
    }
    return render(request, 'home/view_notification.html', context)


@login_required
def delete_notification(request, note_id):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))
    notification = Notification.objects.get(pk=note_id)
    notification.delete()
    return redirect(reverse('all_notifications'))


@login_required
def delete_all_unread_notifications(request):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))
    all_notes = Notification.objects.all()
    for note in all_notes:
        if note.read:
            note.delete()
    return redirect(reverse('all_notifications'))
