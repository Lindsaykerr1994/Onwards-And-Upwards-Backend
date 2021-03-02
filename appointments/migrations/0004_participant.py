# Generated by Django 3.1.6 on 2021-03-02 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_appointment_issolo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('date_of_birth', models.DateField()),
                ('address_line', models.CharField(max_length=254)),
                ('postcode', models.CharField(max_length=10)),
                ('emergency_contact_name', models.CharField(max_length=64)),
                ('emergency_contact_number', models.CharField(max_length=20)),
                ('declaration_illness', models.CharField(blank=True, max_length=254, null=True)),
                ('declaration_medication', models.CharField(blank=True, max_length=254, null=True)),
                ('declaration_absence_cond', models.BooleanField(default=False)),
                ('acknowledgement_of_risk', models.BooleanField(default=False)),
                ('signed_by', models.CharField(max_length=64)),
                ('date_signed', models.DateField()),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appointments.appointment')),
            ],
        ),
    ]
