# Generated by Django 3.1.6 on 2021-03-24 14:24

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_delete_riskacknowledgement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
