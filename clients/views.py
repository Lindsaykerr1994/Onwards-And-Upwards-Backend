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
    for app in apps:
        if app.appointment_date < today:
            past_apps.append(app)
    context = {
        'client': client,
        'root_of_inquiry': client.get_root_of_inquiry_display(),
        'up_apps': up_apps,
        'past_apps': past_apps,
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
            client = form.save()
            messages.success(request, 'Successfully added client')
            return redirect(reverse('view_client', args=[client.id]))
        else:
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
