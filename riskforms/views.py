import uuid
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Participant
from .forms import ParticipantForm
from appointments.models import Appointment
from clients.models import Client


@login_required
def all_participants(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, You don't have permission to do that.")
        return redirect(reverse('home'))
    participants = Participant.objects.all()
    query = None
    sort = None
    direction = None
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'date':
                sortkey = 'appointment_date'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            participants = participants.order_by(sortkey)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('all_participants'))
            queries = Q(participant__last_name__icontains=query) | Q(participant__first_name__icontains=query)
            participants = participants.filter(queries)
    context = {
        'participants': participants
    }
    return render(request, 'riskforms/all_participants.html', context)


@login_required
def view_participant(request, partId):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    clients = Client.objects.all()
    appointment = None
    client = None
    if request.GET:
        if 'appId' in request.GET:
            appId = request.GET['appId']
            appointment = Appointment.objects.get(appointment_number=appId)
        if 'clientId' in request.GET:
            clientId = request.GET['clientId']
            client = Client.objects.get(pk=clientId)
    participant = Participant.objects.get(pk=partId)
    partApps = participant.appointment.all()
    context = {
        'participant': participant,
        'clients': clients,
        'appointment': appointment,
        'client': client,
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
            full_name = request.POST['first_name'] + " " + request.POST['last_name']
            emer_name = request.POST['emergency_contact_name']
            if full_name == emer_name:
                messages.error(request,
                               ('You cannot make yourself your emergency \
                                contact'))
            else:
                try:
                    participant = Participant.objects.get(
                        first_name__iexact=request.POST['first_name'],
                        last_name__iexact=request.POST['last_name'],
                        date_of_birth__iexact=request.POST['date_of_birth'],
                        email_address__iexact=request.POST['email_address'],
                        phone_number__iexact=request.POST['phone_number'],
                    )
                    changes = False
                    if participant.client:
                        print("testing participant.client")
                    if participant.emergency_contact_name != request.POST['emergency_contact_name']:
                        participant.emergency_contact_name = request.POST['emergency_contact_name']
                        participant.emergency_contact_number = request.POST['emergency_contact_number']
                        changes = True
                    if participant.address_line1 != request.POST['address_line1']:
                        participant.address_line1 = request.POST['address_line1']
                        participant.address_line2 = request.POST['address_line2']
                        participant.address_line3 = request.POST['address_line3']
                        participant.town_or_city = request.POST['town_or_city']
                        participant.postcode = request.POST['postcode']
                        changes = True
                    if participant.dec_abs_cond != request.POST['dec_abs_cond']:
                        participant.dec_medication = request.POST['dec_medication']
                        participant.dec_illness = request.POST['dec_illness']
                        changes = True
                    if changes is True:
                        participant.media_acceptance = request.POST['media_acceptance']
                        participant.acknowledgement_of_risk = request.POST['acknowledgement_of_risk']
                        participant.signed_by = request.POST['signed_by']
                        participant.appointment.add(appointment)
                        _send_confirmation_email(appointment, participant)
                        notification = Notification.objects.create(
                            message = "Participant has successfully registered.",
                            participant = participant,
                            appointment = appointment,
                            reference = appointment.appointment_number,
                            classification = "PAR"
                        )
                        messages.success(request, 'We have found your information from a previous session that you have attended.''However, we noticed some changes in your information, so we have gone ahead and updated that.')
                        return redirect(reverse('risk_form_success',
                                        args=[appointment.appointment_number,
                                                participant.pk]))  
                    else:
                        participant.appointment.add(appointment)
                        messages.success(request, 'We have found your information from a previous session that you have attended'"We're glad to see you back!") 
                        return redirect(reverse('risk_form_success',
                                        args=[appointment.appointment_number,
                                                participant.pk]))
                except Participant.DoesNotExist:
                    partForm = ParticipantForm(request.POST)
                    if partForm.is_valid():
                        participant = partForm.save()
                        participant.appointment.add(appointment)
                        # If appointment is solo, or any has one participant
                        # See if participant and client match
                        if appointment.appointment_participants == 1:
                            client = appointment.client
                            if client.first_name == participant.first_name and client.last_name == participants.last_name:
                                # Client and participant names match
                                # This does not guarantee, but we can assume they are the same
                                participant.client = client
                                participant.save(update_fields=['client'])
                        notification = Notification.objects.create(
                            message = "Participant has successfully registered.",
                            particpant = participant,
                            appointment = appointment,
                            reference = appointment.appointment_number,
                            classification = "PAR"
                        )
                        _send_confirmation_email(appointment, participant)
                        messages.success(request, 'Registration completed. \
                            Thank you!')
                        return redirect(reverse('risk_form_success',
                                        args=[appointment.appointment_number,
                                                participant.pk]))
                    else:
                        print(partForm.errors)
                        messages.error(request,
                                    ('Please check that form is valid'))
        partForm = ParticipantForm()
    context = {
        'appointment': appointment,
        'form': partForm,
    }
    return render(request, 'riskforms/add_risk_form.html', context)


@login_required
def manually_add_participant(request, appointment_number):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, but you do not have the permission to visit this page.')
        return redirect(reverse('home'))
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    if request.method == "POST":
        try:
            participant = Participant.objects.get(
                first_name__iexact=request.POST['first_name'],
                last_name__iexact=request.POST['last_name'],
                date_of_birth__iexact=request.POST['date_of_birth'],
                email_address__iexact=request.POST['email_address'],
                phone_number__iexact=request.POST['phone_number']
            )
            if not participant.client:
                if appointment.appointment_participants == 1:
                    client = appointment.client
                    if participant.first_name == client.first_name and participant.last_name == client.last_name:
                        participant.client = client
                        participant.save(update_fields=['client'])
            participant.appointment.add(appointment)
            return redirect(reverse('view_app', args=[appointment_number]))
        except Participant.DoesNotExist:
            form = ParticipantForm(request.POST)
            if form.is_valid():
                participant = form.save()
                participant.appointment.add(appointment)
                if appointment.appointment_participants == 1:
                    client = appointment.client
                    if participant.first_name == client.first_name and participant.last_name == client.last_name:
                        participant.client = client
                        participant.save(update_fields=['client'])
            else:
                messages.error(request, "There is an error in the form. Please check the values enter and try again.")
    form = ParticipantForm()
    context = {
        'appointment': appointment,
        'form': form
    }
    return render(request, 'riskforms/manual_add_form.html', context)


def _send_confirmation_email(appointment, participant):
    """Send the user a confirmation email"""
    part_email = participant.email_address
    subject = render_to_string(
        'riskforms/email_template/pdf_success_subject.txt',
        {'appointment': appointment})
    body = render_to_string(
        'riskforms/email_template/pdf_success_body.txt',
        {'appointment': appointment, 'participant': participant,
            'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [part_email]
    )


@login_required
def update_raform(request, part_id):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you do not have permission to do \
            this.")
        return redirect(reverse('home'))
    if request.method == "POST":
        participant = Participant.objects.get(pk=part_id)
        form = request.FILES['document']
        participant.manual_form = form
        participant.save(update_fields=['manual_form'])
        return redirect(reverse('view_participant',
                        args=[participant.pk]))


@login_required
def delete_raform(request, part_id):
    if request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    participant = Participant.objects.get(pk=part_id)
    return redirect(reverse('view_participant',
                    args=[participant.pk]))


@login_required
def remove_participant(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))
    if request.method == 'GET':
        partId = request.GET['partId']
        participant = Participant.objects.get(pk=partId)
        appId = request.GET['appId']
        removeApp = Appointment.objects.get(appointment_number=appId)
        participant.appointment.remove(removeApp)
        appointments = participant.appointment.all()
        messages.success(request, f'Successfully removed \
        {participant.first_name} {participant.last_name} as a participant\
            from appointment: {removeApp.appointment_number}')
    return redirect(reverse('view_app', args=[appId]))


@login_required
def delete_participant(request, part_id):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))
    participant = get_object_or_404(Participant, pk=part_id)
    participant.delete()
    messages.success(request, 'Participant deleted!')
    return redirect(reverse('all_parts'))


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
    response['Content-Disposition'] = f'filename="oau_ra_form_{part.first_name}_{part.last_name}_{form_number}.pdf"'
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
        'parts': participants,
        'remaining_forms': remaining_forms
    }
    return render(request, 'riskforms/risk_form_success.html', context)


def risk_form_denied(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    all_parts = Participant.objects.all()
    participants = all_parts.filter(appointment=appointment)
    context = {
        'appointment': appointment,
        'participants': participants
    }
    return render(request, 'riskforms/risk_form_denied.html', context)


def kitlist_and_terms(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)

    context = {
        'appointment': appointment
    }
    return render(request, 'riskforms/kitlist_and_terms.html', context)


def onlykitlist(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    partId = None
    if request.method == "GET":
        partId = request.GET['partId']

    context = {
        'appointment': appointment,
        'partId': partId
    }
    return render(request, 'riskforms/onlykitlist.html', context)
