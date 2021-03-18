import uuid
from django.db import models
from appointments.models import Appointment
from clients.models import Client


class Participant(models.Model):
    appointment = models.ManyToManyField(Appointment)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True,
                               blank=True)
    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    date_of_birth = models.DateField()
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address_line1 = models.CharField(max_length=254, null=False, blank=False)
    address_line2 = models.CharField(max_length=254, null=True, blank=True)
    address_line3 = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=64, null=False, blank=False)
    postcode = models.CharField(max_length=10, null=False, blank=False)
    emergency_contact_name = models.CharField(max_length=64, null=False,
                                              blank=False)
    emergency_contact_number = models.CharField(max_length=20, null=False,
                                                blank=False)
    dec_illness = models.TextField(null=True, blank=True)
    dec_medication = models.TextField(null=True, blank=True)
    dec_abs_cond = models.BooleanField(default=False)
    acknowledgement_of_risk = models.BooleanField(default=False)
    # This needs to be default false so that the client
    # has to manually change it.
    signed_by = models.CharField(max_length=64, null=False, blank=False)
    date_signed = models.DateField()
    manual_form = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
