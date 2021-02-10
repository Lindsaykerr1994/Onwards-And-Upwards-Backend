from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from activities.models import Activity, Course
from .models import Client


def all_clients(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'clients/all_clients.html', context)

@login_required
def add_client(request):
    if request.GET:
        print("Add client functionality")
    context = {
    }
    return render(request, 'clients/add_client.html', context)


def view_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {
        'client': client
    }
    return render(request, 'clients/view_client.html', context)
