# Generated by Django 2.2.3 on 2019-09-12 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kai2', '0005_auto_20190911_1856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('delete_on', models.DateTimeField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('paycode', models.CharField(max_length=20)),
                ('net_amount', models.PositiveIntegerField(default=0)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='checkout', to='kai2.Booking')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
