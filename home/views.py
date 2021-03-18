from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment


@login_required
def index(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, You don't have permission to do that.")
        return redirect(reverse('home'))
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments
    }
    return render(request, 'home/index.html', context)
