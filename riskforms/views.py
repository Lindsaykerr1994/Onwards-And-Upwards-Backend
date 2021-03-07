import io
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import FileResponse
from reportlab.pdfgen import canvas
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
        return redirect(reverse('home'))
    else:
        if request.method == "POST":
            form_data = request.POST
            print(form_data)
            partForm = ParticipantForm(request.POST)
            if partForm.is_valid():
                print("nice")
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
