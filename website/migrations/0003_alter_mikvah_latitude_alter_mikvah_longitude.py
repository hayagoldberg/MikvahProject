# Generated by Django 4.2.1 on 2023-05-17 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_mikvah_latitude_mikvah_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mikvah',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='mikvah',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
