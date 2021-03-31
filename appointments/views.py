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
            if sortkey == 'date':
                sortkey = 'appointment_date'
            if sortkey == 'appNum':
                sortkey = 'appointment_number'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            appointments = appointments.order_by(sortkey)

        # if 'activity' in request.GET:
        #     activities = request.GET['activity'].split(',')
        #     appointments = appointments.filter(activity__name__in=activities)
        #     activities = Activity.objects.filter(name__in=activities)

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
        if app.appointment_date >= today:
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
    rel_apps = appointment.rel_apps.all()
    context = {
        'appointment': appointment,
        'participants': participants,
        'all_parts': all_parts,
        'payments': payments,
        'rel_apps': rel_apps
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
        multiple_dates = request.POST['multiple_dates']
        if multiple_dates:
            dates = request.POST['appointment_date']
            dates = dates.split(",")
            rel_app_nums = []
            for date in dates:
                form_data = {
                    "activity": request.POST['activity'],
                    "course": request.POST['course'],
                    "appointment_date": date,
                    "appointment_time": request.POST['appointment_time'],
                    "appointment_participants": request.POST['appointment_participants'],
                    "appointment_location": request.POST['appointment_location'],
                    "isSolo": request.POST['isSolo'],
                    "appointment_price": request.POST['appointment_price'],
                    "add_notes": request.POST['add_notes']
                }
                form = AppointmentForm(form_data)
                if form.is_valid():
                    appointment = form.save()
                    app_num = _generate_app_number(appointment, client)
                    same_number = _filter_by_appnumber(app_num)
                    if same_number:
                        appointment.delete()
                        messages.error(request, 'There is already any existing booking with the same reference number. If you wish to continue, please delete the existing booking, and re-enter the form.')
                        return redirect(reverse('all_appointments'))
                    appointment.appointment_number = app_num
                    appointment.client = client
                    appointment.save(update_fields=["appointment_number", "client"])
                    messages.success(request, f'Successfully add booking:\
                                    {appointment.appointment_number}')
                    rel_app_nums.append(app_num)
                else:
                    messages.error(request, f'Unable to create booking for date: {date}')
                    print(form.errors)
                    return redirect(reverse('add_app'))
            for app in rel_app_nums:
                appointment = Appointment.objects.get(appointment_number=app)
                for add_num in rel_app_nums:
                    if app != add_num:
                        add_to = Appointment.objects.get(appointment_number=add_num)
                        appointment.rel_apps.add(add_to)
            messages.success(request, f'Successfully created all bookings for client: {client.first_name} {client.last_name}')
            return redirect(reverse('all_appointments'))
        if form.is_valid():
            appointment = form.save()
            # Now we need to create an appointment number
            app_num = _generate_app_number(appointment, client)
            # If everything works to this point, we want to check if there is already another appointment with the same appointment number.
            same_number = _filter_by_appnumber(app_num)
            if same_number:
                # There is an appointment with the same number.
                # Delete this appointment and inform of the error.
                appointment.delete()
                messages.error(request, 'There is already any existing booking with the same reference number. If you wish to continue, please delete the existing booking, and re-enter the form.')
                return redirect(reverse('all_appointments'))
            appointment.appointment_number = app_num
            appointment.client = client
            appointment.save(update_fields=["appointment_number", "client"])
            messages.success(request, 'Successfully added booking!')
            print("We need appointment number here")
            return redirect(reverse('view_app', args=[app_num]))
        else:
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
        'add_app': True
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


def add_participant(request, part_id, appointment_number):
    if not request.user.is_staff:
        messages.error(request, "Sorry, I don't want you doing that.")
        return redirect(reverse('home'))
    participant = Participant.objects.get(pk=part_id)
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    participant.appointment.add(appointment)
    messages.success(request, f'Successfully add {participant.first_name} {participant.last_name} to booking: {appointment.appointment_number}')
    return redirect(reverse('view_app', args=[appointment.appointment_number]))


def _generate_app_number(appointment, client):
    app_date = appointment.appointment_date.strftime("%d-%m-%Y")
    app_date = app_date.split("-")
    date_string = app_date[0]+app_date[1]+app_date[2][2:4]
    course_code = appointment.course.course_code
    course_code = int(course_code)
    if course_code < 10:
        course_code = "0"+str(course_code)
    else:
        course_code = str(course_code)
    abbr = client.abbreviation
    app_num = date_string+abbr+course_code
    return app_num


def _filter_by_appnumber(app_num):
    app_exists = False
    # Get all appointments
    apps = Appointment.objects.all()
    # Filter by appointment_number
    apps = apps.filter(appointment_number=app_num)
    # If there is more than one appointment with this app_num
    # Including the new appointment
    # Then return true
    if len(apps) == 1:
        print("found another appointment")
        app_exists = True
    else:
        print("no other appointments")
    return app_exists


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
