from django.db import models


class Activity(models.Model):

    class Meta:
        verbose_name_plural = 'Activities'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return self.friendly_name


class Course(models.Model):
    course_code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    activity = models.ForeignKey('Activity', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    solo = models.BooleanField()
    length = models.DecimalField(max_digits=3, decimal_places=1,
                                 null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    incl_cert = models.BooleanField(default=False)
    add_notes = models.TextField(default="")

    def __str__(self):
        return self.friendly_name
