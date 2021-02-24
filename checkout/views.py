from django.shortcuts import render
from appointments.models import Appointment


def checkout(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'checkout/checkout.html', context)
