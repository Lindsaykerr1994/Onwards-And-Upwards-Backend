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
    if not request.user.is_superuser:
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
            queries = Q(last_name__icontains=query) | Q(first_name__icontains=query)
            clients = clients.filter(queries)
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
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    client = get_object_or_404(Client, pk=client_id)
    all_apps = Appointment.objects.all()
    apps = all_apps.filter(client=client.pk)
    today = datetime.date.today()
    up_apps = []
    past_apps = []
    for app in apps:
        if app.appointment_date > today:
            up_apps.append(app)
        else:
            past_apps.append(app)
    parts = Participant.objects.all()
    parts = parts.filter(client=client)
    up_part_apps = []
    past_part_apps = []
    if len(parts) > 0:
        p_iter = iter(parts)
        participant = next(p_iter)
        part_apps = participant.appointment.all()
        for app in part_apps:
            if app.appointment_date > today:
                up_part_apps.append(app)
            else:
                past_part_apps.append(app)
        print(up_part_apps, past_part_apps)
    else:
        participant = []
    context = {
        'client': client,
        'root_of_inquiry': client.get_root_of_inquiry_display(),
        'up_apps': up_apps,
        'past_apps': past_apps,
        'participant': participant,
        'up_part_apps': up_part_apps,
        'past_part_apps': past_part_apps
    }
    return render(request, 'clients/view_client.html', context)


@login_required
def add_client(request):
    if not request.user.is_superuser:
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
                newAbbr = newAbbr.upper()
                messages.success(request,
                                 f'Updated client abbreviation to: {newAbbr}')
            client = form.save()
            client.abbreviation = newAbbr
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
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added client')
            return redirect(reverse('view_client', args=[client.pk]))
        else:
            messages.error(request, f'There was a error with the form. \
                Please check that all inputs were valid')
            print("Error, we'll sort it out", form.errors)
    else:
        form = ClientForm(instance=client)
        messages.success(request, f'You are editing {client.first_name} \
                     {client.last_name}')
    template = 'clients/edit_client.html'
    context = {
        "form": form,
        "client": client
    }
    return render(request, template, context)


@login_required
def delete_client(request, client_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    client = get_object_or_404(Client, pk=client_id)
    client.delete()
    messages.success(request, 'Client deleted!')
    return redirect(reverse('all_clients'))


@login_required
def convert_client(request, part_id):
    if not request.user.is_superuser:
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
