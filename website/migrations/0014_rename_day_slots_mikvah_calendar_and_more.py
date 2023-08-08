# Generated by Django 4.2.1 on 2023-06-21 07:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_slots'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slots',
            old_name='day',
            new_name='mikvah_calendar',
        ),
        migrations.RemoveField(
            model_name='slots',
            name='closing_time',
        ),
        migrations.RemoveField(
            model_name='slots',
            name='opening_time',
        ),
        migrations.RemoveField(
            model_name='slots',
            name='slot_end',
        ),
        migrations.RemoveField(
            model_name='slots',
            name='slot_start',
        ),
        migrations.AddField(
            model_name='slots',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2023, 6, 21, 7, 10, 41, 888052, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slots',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2023, 6, 21, 7, 11, 51, 727263, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]