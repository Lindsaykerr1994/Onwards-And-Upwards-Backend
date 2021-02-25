from django.shortcuts import render
from appointments.models import Appointment
from .forms import PaymentForm


def checkout(request, appointment_number):
    appointment = Appointment.objects.get(appointment_number=appointment_number)
    if appointment.isPaid:
        print("Redirect to already paid template")
    else:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            full_name = first_name + " " + last_name
            form_data = {
                'full_name': full_name,
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                'town_or_city': request.POST['town_or_city'],
                'street_address1': request.POST['street_address1'],
                'street_address2': request.POST['street_address2'],
                'county': request.POST['county'],
            }
            form = CheckoutForm(form_data)
            if form.is_valid():
                print("Form is all good here")
            else:
                print("form is not valid", form.errors)
        else:
            print("You know how we be, just loading pages on pages")
        context = {
            'appointment': appointment
        }
    return render(request, 'checkout/checkout.html', context)
