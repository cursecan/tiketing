# Generated by Django 2.2.3 on 2019-07-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rekening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('rek_number', models.CharField(max_length=50, unique=True)),
                ('account_name', models.CharField(blank=True, max_length=100)),
                ('bank_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
