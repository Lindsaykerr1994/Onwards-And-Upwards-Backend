# Generated by Django 3.1.6 on 2021-03-09 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riskforms', '0005_auto_20210307_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raform',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='riskforms.participant'),
        ),
    ]