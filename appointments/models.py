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
    isPaid = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.appointment_number
