# Generated by Django 3.0.3 on 2020-02-24 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomBookings', '0007_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='time_from',
            field=models.TimeField(max_length=4),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='time_to',
            field=models.TimeField(max_length=4),
        ),
    ]