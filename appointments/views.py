from django.shortcuts import render
from activities.models import Activity, Course



def all_appointments(request):
    return render(request, 'appointments/all_appointments.html')


def add_app(request):
    activities = Activity.objects.all()
    courses = Course.objects.all()
    context = {
        'activities': activities,
        'courses': courses
    }
    return render(request, 'appointments/add_app.html', context)
