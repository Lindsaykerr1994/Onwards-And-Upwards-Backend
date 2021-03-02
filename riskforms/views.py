from django.shortcuts import render
from .models import Participant
from .forms import ParticipantForm
from appointments.models import Appointment


def add_participant_form(request, appointment_number):
    """ Check if there are more or equal number of
    appointments compared to participants"""
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    partNum = appointment.appointment_participants
    forms = Participant.objects.all()
    formNum = len(forms)
    if formNum >= partNum:
        print("already sufficient number")
    else:
        print("We can add more forms")
    partForm = ParticipantForm()
    context = {
        'appointment': appointment,
        'form': partForm,
    }
    return render(request, 'riskforms/add_form.html', context)
