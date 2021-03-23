from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class Classification(models.TextChoices):
        PARTICIPANT = 'PAR', _('Participant')
        PAYMENT = 'PAY', _('Payment')

    date_created = models.DateField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    reference = models.CharField(null=False, blank=False, max_length=32)
    classification = models.CharField(max_length=3,
                                      choices=Classification.choices)

    def __str__(self):
        return self.message
