from django.db import models
from django.utils.translation import gettext_lazy as _
from riskforms.models import Participant
from checkout.models import Payment
from appointments.models import Appointment


class Notification(models.Model):
    class Classification(models.TextChoices):
        PARTICIPANT = 'PAR', _('Participant')
        PAYMENT = 'PAY', _('Payment')

    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    reference = models.CharField(null=False, blank=False, max_length=32)
    classification = models.CharField(max_length=3,
                                      choices=Classification.choices)
    appointment = models.ForeignKey(Appointment, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    payment = models.ForeignKey(Payment, null=True, blank=True,
                                on_delete=models.SET_NULL)
    participant = models.ForeignKey(Participant, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
