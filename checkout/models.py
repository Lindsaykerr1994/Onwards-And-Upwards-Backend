import uuid
from django.db import models
from appointments.models import Appointment


class Payment(models.Model):
    receipt_no = models.CharField(max_length=32, null=False, editable=False)
    appointment = models.ForeignKey(Appointment, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=20, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    checkout_total = models.DecimalField(max_digits=10, decimal_places=2,
                                         null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def _generate_receipt_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.receipt_no:
            self.receipt_no = self._generate_receipt_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_no


class RiskAcknowledgement(models.Model):
    acknowledgement_no = models.CharField(max_length=32, null=False,
                                          blank=False)
    appointment_no = models.ForeignKey(Appointment, null=False,
                                       blank=False, on_delete=models.CASCADE,
                                       related_name='riskacknowledgement')
    date_created = models.DateField(auto_now_add=True)
    form_pdf_url = models.URLField(max_length=1024, null=True, blank=True)
    form_pdf = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.acknowledgement_no
