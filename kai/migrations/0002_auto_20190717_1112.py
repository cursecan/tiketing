# Generated by Django 2.2.3 on 2019-07-17 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='catched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quotation',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'In Pregress'), (2, 'Catched'), (0, 'Closed')], default=1),
        ),
    ]
