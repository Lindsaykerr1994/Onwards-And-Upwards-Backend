from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from appointments.models import Appointment
from riskforms.models import Participant
from home.models import Notification
from .models import Payment
from .forms import PaymentForm
import stripe


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        appointment_number = request.POST.get('appointment_no')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'appointment_number': appointment_number
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


def checkout(request, appointment_number):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    rel_apps = []
    if appointment.isPaid:
        return redirect(reverse('already_paid', args=[appointment_number]))
    else:
        if request.method == "POST":
            multiple = False
            form_data = {
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                'town_or_city': request.POST['town_or_city'],
                'street_address1': request.POST['street_address1'],
                'street_address2': request.POST['street_address2'],
                'county': request.POST['county']
            }
            form = PaymentForm(form_data)
            if form.is_valid():
                pid = request.POST.get('client_secret').split('_secret')[0]
                multi = request.POST['multiple']
                payment = form.save()
                payment.stripe_pid = pid
                apps = []
                if multi == "true":
                    rel_nums = request.POST['appointment_number']
                    rel_nums = rel_nums.split("/")
                    rel_nums.pop()
                    multiple = True
                    for num in rel_nums:
                        num = num[0:11]
                        app = Appointment.objects.get(appointment_number=num)
                        apps.append(app)
                        payment.appointment.add(app)
                        app.isPaid = True
                        app.save(update_fields=['isPaid'])
                    notification = Notification.objects.create(
                        message="Appointments has been successfully paid for.",
                        reference=payment.receipt_no,
                        payment=payment,
                        classification="PAY"
                    )
                    for app in apps:
                        notification.appointment.add(app)
                    print("Sending multi confirmation")
                    _send_multiconfirmation_email(payment, apps)
                else:
                    payment.appointment.add(appointment)
                    appointment.isPaid = True
                    appointment.save(update_fields=["isPaid"])
                    print("Sending confirmation")
                    _send_confirmation_email(payment)
                    notification = Notification.objects.create(
                        message="Appointment has been successfully paid for.",
                        reference=payment.receipt_no,
                        payment=payment,
                        classification="PAY",
                    )
                    notification.appointment.add(appointment)
                payment.checkout_total = request.POST['checkout_total']
                payment.save(update_fields=["checkout_total", "stripe_pid"])
                print("Updated payment")
                return redirect(reverse('checkout_success',
                                args=[payment.receipt_no]))
            else:
                messages.error(request, ('There was an error with your form. '
                                         'Please double check your \
information.'))
                print(form.errors)
        else:
            multiple = False
            if request.method == "GET":
                multiApps = request.GET.get('multiple')
                if multiApps == "true":
                    multiple = True
                    appNums = request.GET.get('appId')
                    appNums = appNums.split(" ")
                    for num in appNums:
                        app = Appointment.objects.get(appointment_number=num)
                        rel_apps.append(app)
            if multiApps != "true":
                total = appointment.appointment_price
                stripe_total = round(total * 100)
            else:
                total = 0
                for app in rel_apps:
                    total += app.appointment_price
                stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
            form = PaymentForm()
        if not stripe_public_key:
            messages.warning(request, 'Stripe Public Key is missing')
    form = PaymentForm()
    context = {
        'form': form,
        'appointment': appointment,
        'multiple': multiple,
        'rel_apps': rel_apps,
        'total': total,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, receipt_no):
    payment = get_object_or_404(Payment, receipt_no=receipt_no)
    appNums = payment.appointment.all()
    apps = []
    appStr = ""
    multiple = False
    for num in appNums:
        appointment = Appointment.objects.get(appointment_number=num)
        apps.append(appointment)
        appStr += f'{num}+'
    if len(apps) > 1:
        multiple = True
    appStr = appStr[:-1]
    print(appStr)
    appointment = apps[0]
    participants = Participant.objects.all()
    participants = participants.filter(appointment=appointment)
    if participants:
        partLen = len(participants)
        remaining_forms = appointment.appointment_participants - partLen
    else:
        remaining_forms = 0
    context = {
        'payment': payment,
        'appointment': appointment,
        'multiple': multiple,
        'appointments': apps,
        'appStr': appStr,
        'participants': participants,
        'remaining_forms': remaining_forms
    }
    return render(request, 'checkout/checkout_success.html', context)


def already_paid(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    context = {
        'appointment': appointment
    }
    return render(request, 'checkout/already_paid.html', context)


@login_required
def send_payment_request(request, appointment_number):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you don't have permission to do this.")
        return redirect(reverse('home'))
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    appointment.paymentRequest += 1
    appointment.save(update_fields=['paymentRequest', 'paymentSent'])
    """Send the user a confirmation email"""
    cust_email = appointment.client.email_address
    subject = render_to_string(
        'checkout/email_template/payment_request_subject.txt',
        {'appointment': appointment})
    body = render_to_string(
        'checkout/email_template/payment_request_body.txt',
        {'appointment': appointment,
         'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return redirect(reverse('view_app', args=[appointment_number]))


@login_required
def send_multiple_requests(request, appointment_numbers):
    if not request.user.is_staff:
        messages.error(request, "Sorry, you don't have permission to do this.")
        return redirect(reverse('home'))
    if request.method == "GET":
        currApp = request.GET.get('currApp')
    appNums = appointment_numbers.split(",")
    appDates = []
    total_price = 0
    for num in appNums:
        appointment = Appointment.objects.get(appointment_number=num)
        total_price += appointment.appointment_price
        appDates.append(appointment.appointment_date)
        appointment.paymentRequest += 1
        appointment.save(update_fields=['paymentRequest'])
    currAppObj = Appointment.objects.get(appointment_number=currApp)
    cust_email = currAppObj.client.email_address
    subject = render_to_string(
        'checkout/email_template/payment_multi_subject.txt',
        {'appNums': appNums})
    body = render_to_string(
        'checkout/email_template/payment_multi_body.txt',
        {'appointment': currAppObj,
         'appNums': appNums,
         'appDates': appDates,
         'total_price': total_price,
         'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return redirect(reverse('view_app', args=[currApp]))


def _send_confirmation_email(payment):
    """Send the user a confirmation email"""
    cust_email = payment.email
    subject = render_to_string(
        'checkout/email_template/payment_success_subject.txt',
        {'payment': payment})
    body = render_to_string(
        'checkout/email_template/payment_success_body.txt',
        {'payment': payment, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )


def _send_multiconfirmation_email(payment, rel_apps):
    """Send the user a confirmation email"""
    firstApp = rel_apps[0]
    cust_email = payment.email
    subject = render_to_string(
        'checkout/email_template/payment_success_subject.txt',
        {'payment': payment})
    body = render_to_string(
        'checkout/email_template/payment_multisuccess_body.txt',
        {'payment': payment, 'firstApp': firstApp, 'rel_apps': rel_apps,
         'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
