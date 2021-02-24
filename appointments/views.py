from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment
from activities.models import Activity, Course
from clients.models import Client
from clients.forms import ClientForm


@login_required
def all_appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/all_appointments.html', context)


@login_required
def view_appoinment(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'appointments/view_appointment.html', context)


@login_required
def add_app(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        clientNum = request.POST.get('client_select')
        print(clientNum)
        if clientNum is None:
            client_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email_address': request.POST['email'],
                'phone_number': request.POST['phone'],
                'root_of_inquiry': "OTH"
            }
            clientForm = ClientForm(client_data)
            if clientForm.is_valid():
                client = clientForm.save()
                clientNum = client.id
            else:
                print(clientForm.errors)
                messages.error(request,
                               ('Please check that form is valid'))
        else:
            print("Client exists, add foreign key to appointment")
        if form.is_valid():
            app_date = request.POST['appointment_date']
            app_date = app_date.split("-")
            ap = app_date[2]+app_date[1]+app_date[0][2:4]
            client = Client.objects.get(pk=clientNum)
            courseCode = request.POST['course']
            courseCode = int(courseCode)
            if courseCode < 10:
                courseCode = "0"+str(courseCode)
            else:
                courseCode = str(courseCode)
            appNum = ap+client.last_name[0:3].upper()+courseCode
            appointment = form.save()
            appointment.appointment_number = appNum
            appointment.client = clientNum
            appointment.save(update_fields=["appointment_number", "client"])
            messages.success(request, 'Successfully added appointment')
            return redirect(reverse('view_app',
                                    args=[appointment.appointment_number]))
        else:
            print(form.errors, "errors in form")
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
