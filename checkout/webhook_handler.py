from django.conf import settings
from django.http import HttpResponse
from appointments.models import Appointment
from .models import Payment
from django.core.mail import send_mail
from django.template.loader import render_to_string

import time


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, payment):
        """Send the user a confirmation email"""
        cust_email = payment.email
        subject = render_to_string(
            'checkout/email_template/payment_success_subject.txt',
            {'payment': payment})
        body = render_to_string(
            'checkout/email_templatepayment_success_body.txt',
            {'payment': payment, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):
        intent = event.data.object
        print(intent)
        pid = intent.id
        billing_details = intent.charges.data[0].billing_details
        appointment_number = intent.metadata.appointment_number
        checkout_total = round(intent.charges.data[0].amount / 100, 2)
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        payment_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                payment = Payment.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    checkout_total=checkout_total,
                    stripe_pid=pid,
                )
                payment_exists = True
                break
            except Payment.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if payment_exists:
            self._send_confirmation_email(payment)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified in database',
                    status=200)
        else:
            payment = None
            try:
                appointment = Appointment.objects.get(appointment_number=appointment_number)
                payment = Payment.objects.create(
                    appointment=appointment,
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    checkout_total=checkout_total,
                    stripe_pid=pid,
                )
                appointment.isPaid = True
                appointment.save(update_fields=['isPaid'])
            except Exception as e:
                if payment:
                    payment.delete()
                print("tried and failed")
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)
        print("something here")
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Verified in database', status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )
