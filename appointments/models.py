from django.db import models
from activities.models import Activity, Course
from clients.models import Client


class Appointment(models.Model):
    appointment_number = models.CharField(max_length=11, null=False,
                                          blank=False)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,
                               null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    isSolo = models.BooleanField(default=True)
    appointment_participants = models.SmallIntegerField(null=False,
                                                        blank=False, default=1)
    appointment_location = models.CharField(max_length=254, null=True,
                                            blank=True)
    appointment_price = models.DecimalField(max_digits=6, decimal_places=2,
                                            null=False, default=0)
    add_notes = models.TextField(null=True, blank=True)
    isPaid = models.BooleanField(default=False, null=False, blank=False)
    paymentRequest = models.SmallIntegerField(null=False, blank=False,
                                              default=0)
    paymentSent = models.DateTimeField(auto_now=True)
    rel_apps = models.ManyToManyField('self')

    def __str__(self):
        return self.appointment_number
