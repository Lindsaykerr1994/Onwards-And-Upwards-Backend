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
    if not request.user.is_staff:
        messages.error(request, "Sorry, You don't have permission to do that.")
        return redirect(reverse('home'))
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
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    payments = []
    if appointment.isPaid:
        all_payments = Payment.objects.all()
        payments = all_payments.filter(appointment=appointment)
    all_parts = Participant.objects.all()
    participants = all_parts.filter(appointment=appointment)
    context = {
        'appointment': appointment,
        'participants': participants,
        'payments': payments
    }
    return render(request, 'appointments/view_appointment.html', context)


@login_required
def add_app(request):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you do not have permission\
         to access this page.")
        return redirect(reverse('home'))
    if request.method == "POST":
        clientNum = request.POST['client']
        # If there is no client selected, this value with be 0 be default
        if clientNum == "0":
            # No client selected
            # Search if there is a client with the same details
            try:
                client = Client.objects.get(
                    first_name__iexact=request.POST['first_name'],
                    last_name__iexact=request.POST['last_name'],
                    email_address__iexact=request.POST['email'],
                    phone_number__iexact=request.POST['phone']
                )
                messages.info(request, 'Found client profile with matching \
                information. We have used this client to create this booking.')
            except Client.DoesNotExist:
                # Create client profile
                client = None
                try:
                    # Need to find suitable client abbreviation
                    # Where clientAbbr will = return of function
                    last_name = request.POST['last_name']
                    clientAbbr = _generate_client_abbreviation(last_name)
                    client = Client.objects.create(
                        first_name=request.POST['first_name'],
                        last_name=last_name,
                        abbreviation=clientAbbr,
                        email_address=request.POST['email'],
                        phone_number=request.POST['phone'],
                        street_address1="N/A",
                        street_address2="N/A",
                        town_or_city="N/A",
                        postcode="N/A",
                        additional_info="Created through appointment page",
                        root_of_inquiry="OTH"
                    )
                except:
                    # Client cannot be created, return to form.
                    messages.error(request, 'Was not able to create client profile. Please check form and try again.')
                    return redirect(reverse('add_app'))
        else:
            # Find client using the value entered in the form
            client = Client.objects.get(pk=clientNum)
        # By this point, client has been either:
        # Selected in the form using dropdown
        # Founnd using the entered information
        # Created using the entered information
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # Now we need to create an appointment number
            app_num = _generate_app_number(appointment, client)
            appointment.appointment_number = app_num
            appointment.client = client
            appointment.save(update_fields=["appointment_number", "client"])
            messages.success(request, 'Successfully added booking!')
            return redirect(reverse('view_app', args=[app_num]))
        else:
            print(form.errors)
            messages.error(request, 'Unable to create booking. Please check \
            that the form is valid.')
    if request.method == "GET":
        clientId = request.GET.get('clientId',0)
        if clientId != 0:
            client = Client.objects.get(pk=clientId)
        else:
            client = []
    form = AppointmentForm()
    activities = Activity.objects.all()
    courses = Course.objects.all()
    clients = Client.objects.all()
    context = {
        'activities': activities,
        'courses': courses,
        'clients': clients,
        'client': client,
        'form': form,
    }
    return render(request, 'appointments/add_app.html', context)


@login_required
def edit_app(request, appointment_number):
    if not request.user.is_staff:
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
    if not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    appointment = get_object_or_404(Appointment,
                                    appointment_number=appointment_number)
    appointment.delete()
    messages.success(request, 'Appointment deleted!')
    return redirect(reverse('all_appointments'))


@login_required
def mark_as_paid(request, appointment_number):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    appointment.isPaid = True
    appointment.save(update_fields=["isPaid"])
    messages.success(request, 'Marked as paid!')
    return redirect(reverse('view_app',
                            args=[appointment.appointment_number]))


def _generate_app_number(appointment, client):
    app_date = appointment.appointment_date.strftime("%d-%m-%Y")
    app_date = app_date.split("-")
    date_string = app_date[2]+app_date[1]+app_date[0][2:4]
    course_code = appointment.course.course_code
    course_code = int(course_code)
    if course_code < 10:
        course_code = "0"+str(course_code)
    else:
        course_code = str(course_code)
    abbr = client.abbreviation
    app_num = date_string+abbr+course_code
    return app_num


def _generate_client_abbreviation(last_name):
    abbr = last_name[0:3]
    abbr = abbr.upper()
    client_exists = False
    try:
        client = Client.objects.get(abbreviation=abbr)
        client_exists = True
    except Client.DoesNotExist:
        return abbr
    if client_exists:
        # Client with this abbreviation
        # Try another combination
        a = 0
        lLN = len(last_name)
        # where abbr = last_name[a]+last_name[b]+last_name[c]
        while a < (lLN-2):
            b = a+1
            while b < (lLN-1):
                c = b+1
                while c < lLN:
                    # Iterate through possible values for c
                    abbr = last_name[a]+last_name[b]+last_name[c]
                    abbr = abbr.upper()
                    try:
                        client = Client.objects.get(abbreviation=abbr)
                        # If client exists c+=1
                        c += 1
                    except Client.DoesNotExist:
                        # If no client exists
                        return abbr
                b += 1
            a += 1
        if client_exists:
            # If we go through all possibilities for the abbreviation
            # Set a default abbreviation and tell staff to manually update
            abbr = "ZZZ"
            client_exists = False
    else:
        # No client with this abbreviation exists
        return abbr
