from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
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
