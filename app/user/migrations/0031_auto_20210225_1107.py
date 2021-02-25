# Generated by Django 3.1.2 on 2021-02-25 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_auto_20210225_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paypal_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Paypal subscription id'),
        ),
        migrations.AddField(
            model_name='user',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Stripe subscription id'),
        ),
    ]
