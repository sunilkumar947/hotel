# Generated by Django 5.1.5 on 2025-01-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_adminapp', '0006_remove_rooms_check_in_remove_rooms_check_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelroomtype',
            name='room_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
