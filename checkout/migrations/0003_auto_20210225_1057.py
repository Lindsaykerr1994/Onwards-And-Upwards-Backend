# Generated by Django 3.1.6 on 2021-02-25 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20210225_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskacknowledgement',
            name='form_pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='riskacknowledgement',
            name='form_pdf_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
