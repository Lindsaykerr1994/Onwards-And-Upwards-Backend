from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from activities.models import Activity, Course
from .models import Client
from .forms import ClientForm


@login_required
def all_clients(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'clients/all_clients.html', context)


@login_required
def view_client(request, client_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    client = get_object_or_404(Client, pk=client_id)
    context = {
        'client': client,
        'root_of_inquiry': client.get_root_of_inquiry_display()
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
            print("Editted client successfully")
            return redirect(reverse('view_client', args=[client.pk]))
        else:
            print("Error, we'll sort it out", form.errors)
    else:
        form = ClientForm(instance=client)
        print("you are editting client: {client.first_name}")
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
