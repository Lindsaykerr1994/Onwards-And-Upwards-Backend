import uuid
from django.db import models
from appointments.models import Appointment
from clients.models import Client


class Participant(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                    null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True,
                               blank=True)
    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    date_of_birth = models.DateField()
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address_line1 = models.CharField(max_length=254, null=False, blank=False)
    address_line2 = models.CharField(max_length=254, null=True, blank=True)
    address_line3 = models.CharField(max_length=254, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=False, blank=False)
    emergency_contact_name = models.CharField(max_length=64, null=False,
                                              blank=False)
    emergency_contact_number = models.CharField(max_length=20, null=False,
                                                blank=False)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class RAForm(models.Model):
    form_number = models.CharField(max_length=32, null=False, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE,
                                    null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    date_of_birth = models.DateField()
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address_line1 = models.CharField(max_length=254, null=False, blank=False)
    address_line2 = models.CharField(max_length=254, null=True, blank=True)
    address_line3 = models.CharField(max_length=254, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=False, blank=False)
    emergency_contact_name = models.CharField(max_length=64, null=False,
                                              blank=False)
    emergency_contact_number = models.CharField(max_length=20, null=False,
                                                blank=False)
    dec_illness = models.CharField(max_length=254, null=True, blank=True)
    dec_medication = models.CharField(max_length=254, null=True, blank=True)
    dec_abs_cond = models.BooleanField(default=False)
    acknowledgement_of_risk = models.BooleanField(default=False)
    # This needs to be default false so that the client
    # has to manually change it.
    signed_by = models.CharField(max_length=64, null=False, blank=False)
    date_signed = models.DateField()
    risk_form = models.FileField(null=True, blank=True)

    def _generate_form_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.form_number:
            self.form_number = self._generate_form_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.form_number
