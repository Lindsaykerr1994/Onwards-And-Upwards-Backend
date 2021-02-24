from django.shortcuts import render
from appointments.models import Appointment


def checkout(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    if appointment.isPaid:
        print("Redirect to already paid template")
    else:
        print("Allow client to pay")
        context = {
            'appointment': appointment
        }
    return render(request, 'checkout/checkout.html', context)
