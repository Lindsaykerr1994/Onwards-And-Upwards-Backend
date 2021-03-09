import io
from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
from .models import Participant
from .forms import ParticipantForm, RiskAcknowledgementForm
from appointments.models import Appointment


def add_participant_form(request, appointment_number):
    """ Check if there are more or equal number of
    appointments compared to participants"""
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    partNum = appointment.appointment_participants
    allParts = Participant.objects.all()
    participants = allParts.filter(appointment=appointment)
    formNum = len(participants)
    if formNum >= partNum:
        print("Already filled in the number of forms required")
        return redirect(reverse('home'))
    else:
        if request.method == "POST":
            form_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'date_of_birth': request.POST['date_of_birth'],
                'email_address': request.POST['email_address'],
                'phone_number': request.POST['phone_number'],
                'address_line1': request.POST['address1'],
                'address_line2': request.POST['address2'],
                'address_line3': request.POST['address3'],
                'town_or_city': request.POST['town_or_city'],
                'postcode': request.POST['postcode'],
                'emergency_contact_name': request.POST['emergency_name'],
                'emergency_contact_number': request.POST['emergency_number']
            }
            full_name = form_data['first_name'] + " " + form_data['last_name']
            emer_name = form_data['emergency_contact_name']
            if full_name == emer_name:
                print("emergency contact error")
                messages.error(request,
                               ('You cannot make your emergency contact\
                                yourself'))
            else:
                partForm = ParticipantForm(form_data)
                if partForm.is_valid():
                    print("Part Form valid")
                    participant = partForm.save()
                    participant.appointment = appointment
                    participant.save(update_fields=['appointment'])
                    raform_data = {
                        'participant': participant,
                        'first_name': request.POST['first_name'],
                        'last_name': request.POST['last_name'],
                        'date_of_birth': request.POST['date_of_birth'],
                        'email_address': request.POST['email_address'],
                        'phone_number': request.POST['phone_number'],
                        'address_line1': request.POST['address1'],
                        'address_line2': request.POST['address2'],
                        'address_line3': request.POST['address3'],
                        'town_or_city': request.POST['town_or_city'],
                        'postcode': request.POST['postcode'],
                        'emergency_contact_name': request.POST['emergency_name'],
                        'emergency_contact_number': request.POST['emergency_number'],
                        'dec_illness': request.POST['dec_illness'],
                        'dec_medication': request.POST['dec_med'],
                        'dec_abs_cond': request.POST['dec_abs_cond'],
                        'acknowledgement_of_risk': request.POST['ack_of_risk'],
                        'signed_by': request.POST['signed_by'],
                        'date_signed': request.POST['date_signed']
                    }
                    raForm = RiskAcknowledgementForm(raform_data)
                    if raForm.is_valid():
                        raForm.save()
                        print("raForm valid")
                        raFile = create_riskack_form(
                                                     appointment_number,
                                                     form_data)
                        raForm.risk_form = raFile
                        print(raFile)
                    else:
                        print("not valid RAFORM")
                        print(raForm.errors)
                        participant.delete()
                else:
                    print("Error with form", partForm.errors)
                    messages.error(request,
                                   ('Please check that form is valid'))
        partForm = ParticipantForm()
    context = {
        'appointment': appointment,
        'form': partForm,
    }
    return render(request, 'riskforms/add_risk_form.html', context)


def create_riskack_form(appointment_number, form_data):
    pdf = canvas.Canvas("test.pdf")
    pdf.setTitle("myTest")
    pdf.showPage()
    pdf.save()
    return pdf
