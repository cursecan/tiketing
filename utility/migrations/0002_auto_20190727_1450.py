# Generated by Django 2.2.3 on 2019-07-27 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rekening',
            name='rek_number',
            field=models.CharField(max_length=50),
        ),
    ]