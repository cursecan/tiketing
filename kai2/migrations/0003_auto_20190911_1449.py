# Generated by Django 2.2.3 on 2019-09-11 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kai2', '0002_booking_passenger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Open Booking'), (2, 'Waiting List'), (3, 'Waiting Payment'), (4, 'Paid'), (5, 'Finish'), (9, 'Drop')], default=1, editable=False),
        ),
    ]
