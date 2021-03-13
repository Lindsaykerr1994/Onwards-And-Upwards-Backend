import io
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
from .models import Participant, RAForm
from .forms import ParticipantForm, RiskAcknowledgementForm
from appointments.models import Appointment
from clients.models import Client


@login_required
def view_participant(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    if request.method == "GET":
        partId = request.GET['partId']
        appId = request.GET['appId']

        participant = Participant.objects.get(pk=partId)
        appointment = Appointment.objects.get(appointment_number=appId)
        partApps = participant.appointment.all()
    else:
        participant = []
        partApps = []
        appointment = Appointment.objects.all()
    clients = Client.objects.all()
    context = {
        'participant': participant,
        'clients': clients,
        'appointment': appointment,
        'partApps': partApps
    }
    return render(request, 'riskforms/view_participant.html', context)


def add_participant_form(request, appointment_number):
    """ Check if there are more or equal number of
    appointments compared to participants"""
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    partNum = appointment.appointment_participants
    allParts = Participant.objects.all()
    participants = allParts.filter(appointment=appointment)
    formNum = len(participants)
    if formNum >= partNum:
        return redirect(reverse('risk_form_denied',
                        args=[appointment_number]))
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
                messages.error(request,
                               ('You cannot make your emergency contact\
                                yourself'))
                return redirect(reverse('add_part_form',
                               args=[appointment_number]))
            else:
                partForm = ParticipantForm(form_data)
                if partForm.is_valid():
                    print("Part Form valid")
                    participant = partForm.save()
                    participant.appointment.add(appointment)
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
                        raForm.save()
                        return redirect(reverse('risk_form_success',
                                       args=[participant.pk]))
                    else:
                        print("not valid RAFORM")
                        print(raForm.errors)
                        participant.delete()
                        messages.error(request,
                                       ('There is an error with the form. Please check\
                                you have entered a valid input.'))
                        return redirect(reverse('add_part_form',
                                        args=[appointment_number]))
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
    pdf.save()
    return pdf


def risk_form_success(request, part_id):
    participant = get_object_or_404(Participant, pk=part_id)
    ra_form = RAForm.objects.get(participant=participant)
    context = {
        'participant': participant,
        'ra_form': ra_form
    }
    return render(request, 'riskforms/risk_form_success.html', context)


def risk_form_denied(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'riskforms/risk_form_denied.html', context)
