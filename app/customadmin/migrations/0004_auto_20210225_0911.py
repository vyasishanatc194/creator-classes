# Generated by Django 3.1.2 on 2021-02-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0003_availabletimezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='paypal_plan_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='stripe_plan_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
