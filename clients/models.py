from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    street_address1 = models.CharField(max_length=254, null=True, blank=True)
    street_address2 = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=254, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    root_of_inquiry = models.CharField(max_length=254, null=False, blank=False,
                                       default="Other")

    def __str__(self):
        return (self.last_name + ", " + self.first_name)
