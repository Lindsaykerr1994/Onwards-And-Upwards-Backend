from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    class Inquiry(models.TextChoices):
        REFERRAL = 'REF', _('Referral')
        EMAIL = 'EML', _('Email')
        WEBSITE = 'WEB', _('Website')
        PHONE = 'PHO', _('Phone')
        FACEBOOK = 'FAB', _('Facebook')
        FACETOFACE = 'F2F', _('Face To Face')
        INSTAGRAM = 'INS', _('Instagram')
        TWITTER = 'TWT', _('Twitter')
        OTHER = 'OTH', _('Other')

    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    street_address1 = models.CharField(max_length=254, null=True, blank=True)
    street_address2 = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=254, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    root_of_inquiry = models.CharField(max_length=3, choices=Inquiry.choices,
                                       default=Inquiry.OTHER)

    def __str__(self):
        return (self.last_name + ", " + self.first_name)
