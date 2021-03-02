from django.shortcuts import render


def add_participant_form(request, appointment_number):
    """ Check if there are more or equal number of
    appointments compared to participants"""
    context = {

    }
    return render(request, 'riskforms/add_form.html', context)
