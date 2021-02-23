from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment
from activities.models import Activity, Course
from clients.models import Client


@login_required
def all_appointments(request):
    return render(request, 'appointments/all_appointments.html')


@login_required
def view_appoinment(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'clients/view_appointment.html', context)


@login_required
def add_app(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        clientNum = request.POST.get('client_select')
        if clientNum is None:
            print("no client selected")
        if form.is_valid():
            print("form is valid")
            """appointment = form.save()
            messages.success(request, 'Successfully added client')
            return redirect(reverse('view_appointment',
                                    args=[appointment.appointment_number]))"""
        else:
            messages.error(request,
                           ('Please check that form is valid'))
        context = {
            'form': form
        }
    else:
        form = AppointmentForm()
        activities = Activity.objects.all()
        courses = Course.objects.all()
        clients = Client.objects.all()
        context = {
            'activities': activities,
            'courses': courses,
            'clients': clients,
            'form': form
        }
    return render(request, 'appointments/add_app.html', context)


@login_required
def edit_app(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            print("Editted client successfully")
            return redirect(reverse('view_client',
                                    args=[appointment.appointment_number]))
            """ Use email functionality to update client """
        else:
            print("Error, we'll sort it out", form.errors)
    else:
        form = AppointmentForm(instance=appointment)
        print("you are editting appointment: {appointment.appointment_number}")
    template = 'appointments/edit_app.html'
    context = {
        "form": form,
        "appointment": appointment
    }
    return render(request, template, context)


@login_required
def delete_app(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    appointment.delete()
    messages.success(request, 'Appointment deleted!')
    return redirect(reverse('all_clients'))
