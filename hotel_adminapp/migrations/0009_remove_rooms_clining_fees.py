# Generated by Django 5.1.5 on 2025-02-01 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_adminapp', '0008_bookingdiscount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='clining_fees',
        ),
    ]
