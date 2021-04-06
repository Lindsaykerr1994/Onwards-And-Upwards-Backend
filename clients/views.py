from django import template
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import datetime
from .models import Client
from .forms import ClientForm
from activities.models import Activity, Course
from appointments.models import Appointment
from riskforms.models import Participant

register = template.Library()


@login_required
def all_clients(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    clients = Client.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'last_name'
            if sortkey == 'date':
                sortkey = 'appointment_date'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            clients = clients.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('all_clients'))
            queries = Q(last_name__icontains=query) | Q(first_name__icontains=query) | Q(abbreviation__iexact=query.upper())
            clients = clients.filter(queries)
    if not sort:
        clients = clients.order_by('last_name')
    appointments = Appointment.objects.all()
    appointments = appointments.order_by('-appointment_date')

    context = {
        'clients': clients,
        'current_sorting': sort,
        'current_direction': direction,
        'search_term': query,
        'appointments': appointments,
    }
    return render(request, 'clients/all_clients.html', context)


@login_required
def view_client(request, client_id):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    client = get_object_or_404(Client, pk=client_id)
    participants = Participant.objects.all()
    participants = participants.filter(client=client)
    all_apps = Appointment.objects.all()
    apps = all_apps.filter(client=client.pk)
    add_to_apps = _add_participant_apps(apps, client)
    unfiltered_apps = []
    for app in apps:
        unfiltered_apps.append(app)
    for app in add_to_apps:
        unfiltered_apps.append(app)
    today = datetime.date.today()
    up_apps = []
    past_apps = []
    for app in unfiltered_apps:
        if app.appointment_date >= today:
            up_apps.append(app)
        else:
            past_apps.append(app)
    print(up_apps, past_apps)
    context = {
        'client': client,
        'root_of_inquiry': client.get_root_of_inquiry_display(),
        'up_apps': up_apps,
        'past_apps': past_apps,
        'participants': participants
    }
    return render(request, 'clients/view_client.html', context)


@login_required
def add_client(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            abbr = request.POST['abbreviation']
            all_clients = Client.objects.all()
            all_clients = all_clients.filter(abbreviation=abbr)
            print(all_clients)
            if len(all_clients) != 0:
                newAbbr = request.POST['last_name']
                newAbbr = newAbbr[0]+newAbbr[2]+newAbbr[3]
                abbr = newAbbr.upper()
                if len(all_clients) != 0:
                    messages.info(request,
                                 f'Updated client abbreviation to: {newAbbr}. There is another client with this abbreviation. You will need to declare a new abbreviation.')
                else:
                    messages.success(request,
                                     f'Updated client abbreviation to: {newAbbr}')
            client = form.save()
            client.abbreviation = abbr
            client.save(update_fields=['abbreviation'])
            messages.success(request, 'Successfully added client')
            return redirect(reverse('view_client', args=[client.id]))
        else:
            print(form.errors)
            messages.error(request,
                           ('Please check that form is valid'))
    else:
        form = ClientForm()
    context = {
        "form": form
    }
    return render(request, 'clients/add_client.html', context)


@login_required
def edit_client(request, client_id):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you do not have permission to do this.")
        return redirect(reverse('home'))
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        abbr = request.POST['abbreviation']
        # See if abbreviation has changed
        if abbr != client.abbreviation:
            # Abbreviation has changed
            # Check if new abbreviation is avaiable
            all_clients = Client.objects.all()
            all_clients = all_clients.filter(abbreviation=abbr)
            if len(all_clients) >= 1:
                # Abbreviation is already in use
                messages.error(request, "Unable to update client's abbreviation field as it was already in use.""All other fields have been updated.""Please try another value for abbreviation and resubmit again.")
                # Update client without abbreviation
                form_data = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'abbreviation': client.abbreviation,
                    'email_address': request.POST['email_address'],
                    'phone_number': request.POST['phone_number'],
                    'street_address1': request.POST['street_address1'],
                    'street_address2': request.POST['street_address2'],
                    'town_or_city': request.POST['town_or_city'],
                    'postcode': request.POST['postcode'],
                    'additional_info': request.POST['additional_info'],
                    'root_of_inquiry': request.POST['root_of_inquiry']
                }
                form = ClientForm(form_data, instance=client)
                if form.is_valid:
                    form.save()
                    messages.success(request, 'Successfully updated client')
                    return redirect(reverse('view_client', args=[client.pk]))
                else:
                    messages.error(request, f'There was an error with the form. Was unable to update client: {client.first_name} {client.last_name}')
                    return redirect(reverse('edit_client', args=[client.pk]))
            else:
                form = ClientForm(request.POST, instance=client)
                if form.is_valid:
                    client = form.save()
                    _update_clients_appointments(client)
                    messages.success(request, 'Successfully updated client')
                    return redirect(reverse('view_client', args=[client.pk]))
                else:
                    messages.error(request, f'There was an error with the form. Was unable to update client: {client.first_name} {client.last_name}')
                    return redirect(reverse('edit_client', args=[client.pk])) 
        else:
            form = ClientForm(request.POST, instance=client)
            if form.is_valid:
                form.save()
                messages.success(request, 'Successfully updated client')
                return redirect(reverse('view_client', args=[client.pk]))
            else:
                messages.error(request, f'There was an error with the form. Was unable to update client: {client.first_name} {client.last_name}')
                return redirect(reverse('edit_client', args=[client.pk]))
    else:
        form = ClientForm(instance=client)
        messages.info(request, f'You are editing {client.first_name} {client.last_name}')
    template = 'clients/edit_client.html'
    context = {
        'form': form,
        'client': client
    }
    return render(request, template, context)


@login_required
def delete_client(request, client_id):
    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    client = get_object_or_404(Client, pk=client_id)
    client.delete()
    messages.success(request, 'Client deleted!')
    return redirect(reverse('all_clients'))


@login_required
def convert_client(request, part_id):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))
    if request.method == "GET":
        newClient = request.GET['newClient']
        if newClient == "true":
            appId = request.GET['appId']
            part = Participant.objects.get(pk=part_id)
            abbr = part.last_name[0:3]
            all_clients = Client.objects.all()
            all_clients = all_clients.filter(abbreviation=abbr)
            if len(all_clients) != 0:
                newAbbr = part.last_name
                newAbbr = newAbbr[0]+newAbbr[2]+newAbbr[3]
                newAbbr = newAbbr.upper()
                abbr = newAbbr
            part_data = {
                'first_name': part.first_name,
                'last_name': part.last_name,
                'abbreviation': abbr,
                'email_address': part.email_address,
                'phone_number': part.phone_number,
                'street_address1': part.address_line1,
                'street_address2': part.address_line2,
                'town_or_city': part.town_or_city,
                'postcode': part.postcode,
                'additional_info': 'Created from participant model',
                'root_of_inquiry': 'REF'
            }
            form = ClientForm(part_data)
            if form.is_valid():
                client = form.save()
                part.client = client
                part.save(update_fields=['client'])
                messages.success(request, f'Successfully created client from \
                    participant: {part.first_name} {part.last_name}')
                return redirect(reverse('view_client', args=[client.id]))
            else:
                print(form.errors)
                messages.error(request, "Missing information preventing creation of \
                    client. Please check the participant's information.")
                return redirect(reverse('view_participant',
                                args=[appId, part.pk]))
        else:
            participant = Participant.objects.get(pk=part_id)
            clientId = request.GET['clientId']
            client = Client.objects.get(pk=clientId)
            if client:
                participant.client = client
                participant.save(update_fields=['client'])
                messages.success(request, f'Successfully merged participant \
                    with client to form super client: {client.first_name} \
                        {client.last_name}!')
                return redirect(reverse('view_client', args=[client.id]))
            else:
                messages.error(request, 'Was not able to merge participant \
                    with client. Would you like to create a new client model?')
                return redirect(reverse('view_participant',
                                args=[appId, participant.id]))


def _update_clients_appointments(client):
    all_apps = Appointment.objects.all()
    all_apps = all_apps.filter(client=client)
    for app in all_apps:
        appNum = _generate_app_number(app, client)
        app.appointment_number = appNum
        app.save(update_fields=['appointment_number'])


def _generate_app_number(appointment, client):
    app_date = appointment.appointment_date.strftime("%d-%m-%Y")
    app_date = app_date.split("-")
    date_string = app_date[0]+app_date[1]+app_date[2][2:4]
    course_code = appointment.course.course_code
    course_code = int(course_code)
    if course_code < 10:
        course_code = "0"+str(course_code)
    else:
        course_code = str(course_code)
    abbr = client.abbreviation
    app_num = date_string+abbr+course_code
    return app_num


def _add_participant_apps(apps, client):
    return_apps = []
    all_parts = Participant.objects.all()
    all_parts = all_parts.filter(client=client)
    for part in all_parts:
        part_apps = part.appointment.all()
        for p in part_apps:
            for app in apps:
                if p != app:
                    return_apps.append(p)
    return return_apps
