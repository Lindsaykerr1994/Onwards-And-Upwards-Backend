# Generated by Django 3.1.6 on 2021-03-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_delete_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='add_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]