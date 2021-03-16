from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment
from django.db.models import Q
import datetime
from activities.models import Activity, Course
from clients.models import Client
from clients.forms import ClientForm
from checkout.models import Payment
from riskforms.models import Participant


@login_required
def all_appointments(request):
    appointments = Appointment.objects.all()
    query = None
    activities = None
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
            appointments = appointments.order_by(sortkey)

        if 'activity' in request.GET:
            activities = request.GET['activity'].split(',')
            appointments = appointments.filter(activity__name__in=activities)
            activities = Activity.objects.filter(name__in=activities)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('all_appointments'))
            queries = Q(client__last_name__icontains=query) | Q(client__first_name__icontains=query) | Q(course__name__icontains=query) | Q(activity__name__icontains=query)
            appointments = appointments.filter(queries)
    today = datetime.date.today()
    up_apps = []
    past_apps = []
    for app in appointments:
        if app.appointment_date > today:
            up_apps.append(app)
    for app in appointments:
        if app.appointment_date < today:
            past_apps.append(app)
    context = {
        'up_apps': up_apps,
        'past_apps': past_apps,
        'current_sorting': sort,
        'current_direction': direction,
        'search_term': query
    }
    return render(request, 'appointments/all_appointments.html', context)


@login_required
def view_appoinment(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    payment = []
    if appointment.isPaid:
        payment = Payment.objects.get(appointment=appointment)

    all_parts = Participant.objects.all()
    participants = all_parts.filter(appointment=appointment)
    context = {
        'appointment': appointment,
        'participants': participants,
        'payment': payment
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
        courseId = request.POST['course']
        course = Course.objects.get(pk=courseId)
        if form.is_valid():
            app_date = request.POST['appointment_date']
            app_date = app_date.split("-")
            ap = app_date[2]+app_date[1]+app_date[0][2:4]
            client = Client.objects.get(pk=clientNum)
            courseCode = course.course_code
            courseCode = int(courseCode)
            print(courseCode)
            if courseCode < 10:
                courseCode = "0"+str(courseCode)
            else:
                courseCode = str(courseCode)
            appNum = ap+client.last_name[0:3].upper()+courseCode
            appointment = form.save()
            appointment.appointment_number = appNum
            appointment.client = client
            appointment.save(update_fields=["appointment_number", "client"])
            messages.success(request, 'Successfully added appointment')
            return redirect(reverse('view_app',
                                    args=[appointment.appointment_number]))
        else:
            print(form.errors, "errors in form")
            messages.error(request,
                        ('Please check that form is valid'))
    else:
        form = AppointmentForm()
    activities = Activity.objects.all()
    courses = Course.objects.all()
    clients = Client.objects.all()
    context = {
        'activities': activities,
        'courses': courses,
        'clients': clients,
        'form': form,
        'add_app': True
    }
    return render(request, 'appointments/add_app.html', context)


@login_required
def add_app_w_client(request, client_id):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    client = Client.objects.get(pk=client_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        courseId = request.POST['course']
        course = Course.objects.get(pk=courseId)
        if form.is_valid():
            app_date = request.POST['appointment_date']
            app_date = app_date.split("-")
            ap = app_date[2]+app_date[1]+app_date[0][2:4]
            courseCode = course.course_code
            courseCode = int(courseCode)
            if courseCode < 10:
                courseCode = "0"+str(courseCode)
            else:
                courseCode = str(courseCode)
            appNum = ap+client.last_name[0:3].upper()+courseCode
            appointment = form.save()
            appointment.appointment_number = appNum
            appointment.client = client
            appointment.save(update_fields=["appointment_number", "client"])
            messages.success(request, 'Successfully added appointment')
            return redirect(reverse('view_app',
                                    args=[appointment.appointment_number]))
        else:
            print(form.errors, "errors in form")
            messages.error(request,
                           ('Please check that form is valid'))
    else:
        form = AppointmentForm()
    activities = Activity.objects.all()
    courses = Course.objects.all()
    context = {
        'activities': activities,
        'courses': courses,
        'client': client,
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
        courseId = request.POST['course']
        course = Course.objects.get(pk=courseId)
        if form.is_valid():
            app_date = request.POST['appointment_date']
            app_date = app_date.split("/")
            ap = app_date[0]+app_date[1]+app_date[2][2:4]
            client = appointment.client
            courseCode = course.course_code
            courseCode = int(courseCode)
            if courseCode < 10:
                courseCode = "0"+str(courseCode)
            else:
                courseCode = str(courseCode)
            appNum = ap+client.last_name[0:3].upper()+courseCode
            appointment.appointment_number = appNum
            appointment.save(update_fields=["appointment_number"])
            form.save()
            messages.success(request, f'Successfully edited appointment:\
                {appointment.appointment_number}')
            return redirect(reverse('view_app',
                                    args=[appointment.appointment_number]))
            """ Use email functionality to inform client """
        else:
            print("Error, we'll sort it out", form.errors)
    else:
        form = AppointmentForm(instance=appointment)
        print("you are editting appointment: {appointment.appointment_number}")
    clients = Client.objects.all()
    activities = Activity.objects.all()
    courses = Course.objects.all()
    template = 'appointments/edit_app.html'
    context = {
        "form": form,
        "appointment": appointment,
        "clients": clients,
        "activities": activities,
        "courses": courses
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
    return redirect(reverse('all_appointments'))


@login_required
def mark_as_paid(request, appointment_number):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    appointment.isPaid = True
    appointment.save(update_fields=["isPaid"])
    messages.success(request, 'Marked as paid!')
    return redirect(reverse('view_app',
                            args=[appointment.appointment_number]))
