# Generated by Django 3.1.6 on 2021-02-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20210211_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='town_or_city',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
