# Generated by Django 4.2.1 on 2023-08-06 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0022_appointment3_mikvah_calendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment2',
            name='user',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.DeleteModel(
            name='Appointment2',
        ),
    ]
