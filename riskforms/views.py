import io
from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from .models import Participant
from .forms import ParticipantForm, RiskAcknowledgementForm as RAForm
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
            print(full_name, emer_name)
            if full_name == emer_name:
                messages.error(request,
                               ('You cannot make your emergency contact\
                                yourself'))
            else:
                partForm = ParticipantForm(form_data)
                if partForm.is_valid():
                    print("Form submitted")
                    participant = partForm.save()
                    participant.appointment = appointment
                    participant.save(update_fields=['appointment'])
                    raform_data = {
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
                    raForm = RAForm(raform_data)
                    if raForm.is_valid():
                        print("we can make a pdf now")
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


def create_riskack_form(request, appointment_number):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
