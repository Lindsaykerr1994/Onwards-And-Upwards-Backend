from django.shortcuts import render
from activities.models import Activity, Course
from .models import Client


def all_clients(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'clients/all_clients.html', context)


def add_client(request):
    context = {
    }
    return render(request, 'clients/add_client.html', context)
