# Generated by Django 4.2.1 on 2023-06-22 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_appointment3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment3',
            old_name='mikvah',
            new_name='mikvah_id',
        ),
    ]
