# Generated by Django 2.2.3 on 2019-09-11 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kai2', '0004_auto_20190911_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='passengers', to='kai2.Booking'),
        ),
    ]