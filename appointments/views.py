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
    clientId = None
    if request.GET:
        clientId = request.GET['clientId']
        client = Client.objects.get(pk=clientId)
    else:
        client = []
    if request.method == "POST":
        clientNum = request.POST['client']
        if clientNum is None or clientNum == "0":
            clientLast = request.POST['last_name']
            abbr = clientLast[0:3]
            abbr = abbr.upper()
            all_clients = Client.objects.all()
            all_clients = all_clients.filter(abbreviation=abbr)
            if len(all_clients) != 0:
                newAbbr = request.POST['last_name']
                newAbbr = newAbbr[0]+newAbbr[2]+newAbbr[3]
                abbr = newAbbr.upper()
                all_clients = Client.objects.all()
                all_clients = all_clients.filter(abbreviation=abbr)
                if len(all_clients) != 0:
                    messages.info(request,
                                 f'Updated client abbreviation to: {newAbbr}. There is another client with this abbreviation. You will need to declare a new abbreviation.')
                else:
                    messages.success(request,
                                 f'Updated client abbreviation to: {newAbbr}')
            client_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'abbreviation': abbr,
                'email_address': request.POST['email'],
                'phone_number': request.POST['phone'],
                'root_of_inquiry': "OTH"
            }
            clientForm = ClientForm(client_data)
            if clientForm.is_valid():
                client = clientForm.save()
                clientNum = client.id
                courseId = request.POST['course']
                course = Course.objects.get(pk=courseId)
                form_data = {
                    'activity': request.POST['activity'],
                    'course': request.POST['course'],
                    'client': client,
                    'appointment_date': request.POST['appointment_date'],
                    'appointment_time': request.POST['appointment_time'],
                    'isSolo': request.POST.get('isSolo'),
                    'appointment_participants': request.POST['appointment_participants'],
                    'appointment_location': request.POST['appointment_location'],
                    'appointment_price': request.POST['appointment_price'],
                    'add_notes': request.POST['add_notes']
                }
                form = AppointmentForm(form_data)
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
                    abbr = client.abbreviation
                    appNum = ap+abbr+courseCode
                    appointment = form.save()
                    appointment.client = client
                    appointment.appointment_number = appNum
                    appointment.save(update_fields=["appointment_number", "client"])
                    messages.success(request, 'Successfully added appointment')
                    return redirect(reverse('view_app',
                                            args=[appointment.appointment_number]))
                else:
                    messages.error(request,
                                ('Please check that form is valid'))
            else:
                messages.error(request,
                               ('Could not create a new client,\
therefore could not create appointment.'))
                return redirect(reverse('add_app'))
        else:
            courseId = request.POST['course']
            course = Course.objects.get(pk=courseId)
            form = AppointmentForm(request.POST)
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
                clientNum = request.POST['client']
                client = Client.objects.get(pk=clientNum)
                abbr = client.abbreviation
                appNum = ap+client.abbreviation+courseCode
                appointment = form.save()
                appointment.client = client
                appointment.appointment_number = appNum
                appointment.save(update_fields=["appointment_number", "client"])
                messages.success(request, 'Successfully added appointment')
                return redirect(reverse('view_app',
                                        args=[appointment.appointment_number]))
            else:
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
        'client': client,
        'clients': clients,
        'form': form,
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
            app_date = app_date.split("-")
            ap = app_date[2]+app_date[1]+app_date[0][2:4]
            client = appointment.client
            courseCode = course.course_code
            courseCode = int(courseCode)
            if courseCode < 10:
                courseCode = "0"+str(courseCode)
            else:
                courseCode = str(courseCode)
            appNum = ap+client.abbreviation+courseCode
            appointment.appointment_number = appNum
            appointment.save(update_fields=["appointment_number"])
            form.save()
            messages.success(request, f'Successfully edited appointment:\
                {appointment.appointment_number}')
            return redirect(reverse('view_app',
                                    args=[appointment.appointment_number]))
            """ Use email functionality to inform client """
        else:
            print(form.errors)
            messages.error(request, f'Was not able to update appointment: {appointment.appointment_number} due to errors in the form.')
            return redirect(reverse('edit_app',
                                    args=[appointment.appointment_number]))
    else:
        form = AppointmentForm(instance=appointment)
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
