# Generated by Django 3.1.6 on 2021-04-06 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0013_auto_20210331_1041'),
        ('home', '0005_auto_20210324_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='appointment',
        ),
        migrations.AddField(
            model_name='notification',
            name='appointment',
            field=models.ManyToManyField(to='appointments.Appointment'),
        ),
    ]
