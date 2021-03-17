import uuid
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from .models import Participant, RAForm
from .forms import ParticipantForm, RiskAcknowledgementForm
from appointments.models import Appointment
from clients.models import Client


@login_required
def view_participant(request, appId, partId):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    clients = Client.objects.all()
    participant = Participant.objects.get(pk=partId)
    appointment = Appointment.objects.get(appointment_number=appId)
    raform = RAForm.objects.all()
    for form in raform:
        print(form.participant)
    print(raform)
    partApps = participant.appointment.all()
    context = {
        'participant': participant,
        'raform': raform,
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
                'emergency_contact_number': request.POST['emergency_number'],
                'dec_illness': request.POST['dec_illness'],
                'dec_medication': request.POST['dec_medication'],
                'dec_abs_cond': request.POST['dec_abs_cond'],
                'acknowledgement_of_risk': request.POST['ack_of_risk'],
                'signed_by': request.POST['signed_by'],
                'date_signed': request.POST['date_signed']
            }
            if form_data['address_line2'] is None:
                form_data['address_line2'] = " "
            if form_data['address_line3'] is None:
                form_data['address_line3'] = " "
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
                else:
                    messages.error(request,
                                   ('Please check that form is valid'))
        partForm = ParticipantForm()
    context = {
        'appointment': appointment,
        'form': partForm,
    }
    return render(request, 'riskforms/add_risk_form.html', context)


@login_required
def update_raform(request, part_id, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you do not have permission to do \
            this.")
        return redirect(reverse('home'))
    if request.method == "POST":
        participant = Participant.objects.get(pk=part_id)
        raForm = RAForm.objects.get(participant=participant)
        form = request.FILES['document']
        raForm.risk_form = form
        raForm.save(update_fields=['risk_form'])

        return redirect(reverse('view_appointment', args=[appointment_number]))


@login_required
def delete_raform(request, form_number, part_id, appointment_number):
    form = RAForm.objects.get(form_number=form_number)
    form.delete()
    return redirect(reverse('view_participant',
                    args=[appointment_number, part_id]))


@login_required
def remove_participant(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))
    if request.method == 'GET':
        partId = request.GET['partId']
        participant = Participant.objects.get(pk=partId)
        appId = request.GET['appId']
        removeApp = Appointment.objects.get(appointment_number=appId)
        participant.appointment.remove(removeApp)
        appointments = participant.appointment.all()
        if len(appointments) == 0:
            participant.delete()
            messages.success(request, f'Deleted this participant')
        else:
            messages.success(request, f'Successfully removed \
            {participant.first_name} {participant.last_name} as a participant\
             from appointment: {removeApp.appointment_number}')
    return redirect(reverse('view_app', args=[appId]))


def download_pdf(request, part_id):
    template_path = 'riskforms/pdf_template/risk_acknowledgement.html'
    part = get_object_or_404(Participant, pk=part_id)
    context = {
        'first_name': part.first_name,
        'last_name': part.last_name,
        'date_of_birth': part.date_of_birth,
        'email_address': part.email_address,
        'phone_number': part.phone_number,
        'address_line1': part.address_line1,
        'address_line2': part.address_line2,
        'address_line3': part.address_line3,
        'town_or_city': part.town_or_city,
        'postcode': part.postcode,
        'emergency_contact_name': part.emergency_contact_name,
        'emergency_contact_number': part.emergency_contact_number,
        'dec_illness': part.dec_illness,
        'dec_medication': part.dec_medication,
        'dec_abs_cond': part.dec_abs_cond,
        'acknowledgement_of_risk': part.acknowledgement_of_risk,
        'signed_by': part.signed_by,
        'date_signed': part.date_signed
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    form_number = _generate_form_number()
    response['Content-Disposition'] = f'attachment; filename="\
        oau_ra_form_{part.first_name}_{part.last_name}_{form_number}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def view_pdf(request, part_id):
    template_path = 'riskforms/pdf_template/risk_acknowledgement.html'
    part = get_object_or_404(Participant, pk=part_id)
    context = {
        'first_name': part.first_name,
        'last_name': part.last_name,
        'date_of_birth': part.date_of_birth,
        'email_address': part.email_address,
        'phone_number': part.phone_number,
        'address_line1': part.address_line1,
        'address_line2': part.address_line2,
        'address_line3': part.address_line3,
        'town_or_city': part.town_or_city,
        'postcode': part.postcode,
        'emergency_contact_name': part.emergency_contact_name,
        'emergency_contact_number': part.emergency_contact_number,
        'dec_illness': part.dec_illness,
        'dec_medication': part.dec_medication,
        'dec_abs_cond': part.dec_abs_cond,
        'acknowledgement_of_risk': part.acknowledgement_of_risk,
        'signed_by': part.signed_by,
        'date_signed': part.date_signed
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    form_number = _generate_form_number()
    response['Content-Disposition'] = f'filename="oau_ra_form_\
        {part.first_name}_{part.last_name}_{form_number}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def _generate_form_number():
    return uuid.uuid4().hex.upper()


def risk_form_success(request, appointment_number, part_id):
    participant = get_object_or_404(Participant, pk=part_id)
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    ra_form = RAForm.objects.all()
    participants = Participant.objects.all()
    participants = participants.filter(appointment=appointment)
    if participants:
        partLen = len(participants)
        remaining_forms = appointment.appointment_participants - partLen
    else:
        remaining_forms = 0
    context = {
        'participant': participant,
        'appointment': appointment,
        'ra_form': ra_form,
        'parts': participants,
        'remaining_forms': remaining_forms
    }
    return render(request, 'riskforms/risk_form_success.html', context)


def risk_form_denied(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'riskforms/risk_form_denied.html', context)


def kitlist_and_terms(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)

    context = {
        'appointment': appointment
    }
    return render(request, 'riskforms/kitlist.html', context)
