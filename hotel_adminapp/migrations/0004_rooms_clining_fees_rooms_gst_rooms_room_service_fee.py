# Generated by Django 5.1.5 on 2025-01-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_adminapp', '0003_delete_bookingroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='clining_fees',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='rooms',
            name='gst',
            field=models.IntegerField(choices=[(12, '12%'), (18, '18%')], default=12),
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_service_fee',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
