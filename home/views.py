from django.shortcuts import render
from appointments.models import Appointment


def index(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments
    }
    return render(request, 'home/index.html', context)
