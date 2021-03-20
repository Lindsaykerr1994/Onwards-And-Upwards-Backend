from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from appointments.models import Appointment
from riskforms.models import Participant
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
    if appointment.isPaid:
        return redirect(reverse('already_paid', args=[appointment_number]))
    else:
        if request.method == "POST":
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
                payment = form.save()
                pid = request.POST.get('client_secret').split('_secret')[0]
                payment.stripe_pid = pid
                payment.appointment = appointment
                payment.checkout_total = appointment.appointment_price
                appointment.isPaid = True
                appointment.save(update_fields=['isPaid'])
                payment.save(update_fields=["appointment", "checkout_total",
                             "stripe_pid"])
                return redirect(reverse('checkout_success',
                                args=[payment.receipt_no]))
            else:
                messages.error(request, ('There was an error with your form. '
                                         'Please double check your \
information.'))
        else:
            total = appointment.appointment_price
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
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, receipt_no):
    payment = get_object_or_404(Payment, receipt_no=receipt_no)
    appNumber = payment.appointment
    appointment = Appointment.objects.get(appointment_number=appNumber)
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
    """Send the user a confirmation email"""
    cust_email = appointment.client.email_address
    subject = render_to_string(
        'checkout/email_template/payment_success_subject.txt',
        {'appointment': appointment})
    body = render_to_string(
        'checkout/email_template/payment_success_body.txt',
        {'appointment': appointment,
         'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return redirect(reverse('view_app', args=[appointment_number]))
