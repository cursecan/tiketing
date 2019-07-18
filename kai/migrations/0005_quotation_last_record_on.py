# Generated by Django 2.2.3 on 2019-07-18 09:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kai', '0004_quotation_telegram'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='last_record_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Record'),
        ),
    ]
