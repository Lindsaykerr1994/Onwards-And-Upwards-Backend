# Generated by Django 3.1.6 on 2021-03-16 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskforms', '0010_auto_20210316_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raform',
            name='risk_form',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
