# Generated by Django 3.1.6 on 2021-02-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='root_of_inquiry',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
