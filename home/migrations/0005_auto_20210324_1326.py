# Generated by Django 3.1.6 on 2021-03-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210324_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
