# Generated by Django 4.2.1 on 2023-06-29 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_rename_mikvah_appointment3_mikvah_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment3',
            name='canceled',
            field=models.BooleanField(default=True),
        ),
    ]
