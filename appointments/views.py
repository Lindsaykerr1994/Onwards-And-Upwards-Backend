from django.shortcuts import render
from activities.models import Activity, Course
from clients.models import Client


def all_appointments(request):
    return render(request, 'appointments/all_appointments.html')


def add_app(request):
    activities = Activity.objects.all()
    courses = Course.objects.all()
    clients = Client.objects.all()
    context = {
        'activities': activities,
        'courses': courses,
        'clients': clients,
    }
    return render(request, 'appointments/add_app.html', context)
