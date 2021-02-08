from django.shortcuts import render

# Create your views here.


def all_appointments(request):
    return render(request, 'appointments/all_appointments.html')
