# Generated by Django 3.1.6 on 2021-03-16 14:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('riskforms', '0008_auto_20210316_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raform',
            name='acknowledgement_of_risk',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='address_line3',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='date_signed',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='dec_abs_cond',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='dec_illness',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='dec_medication',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='emergency_contact_name',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='emergency_contact_number',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='raform',
            name='signed_by',
        ),
        migrations.AddField(
            model_name='participant',
            name='acknowledgement_of_risk',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='date_signed',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='dec_abs_cond',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='dec_illness',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='dec_medication',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='signed_by',
            field=models.CharField(default='Lindsay Kerr', max_length=64),
            preserve_default=False,
        ),
    ]