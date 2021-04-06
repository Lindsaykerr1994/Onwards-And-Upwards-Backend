# Generated by Django 3.1.6 on 2021-03-30 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0011_appointment_paymentsent'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='rel_apps',
            field=models.ManyToManyField(related_name='_appointment_rel_apps_+', to='appointments.Appointment'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='paymentSent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]