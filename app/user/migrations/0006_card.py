# Generated by Django 3.1.2 on 2020-12-03 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20201126_0414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(blank=True, max_length=255, verbose_name='Card Id')),
                ('customer_id', models.CharField(blank=True, max_length=255, verbose_name='Customer Id')),
                ('last4', models.CharField(blank=True, max_length=255, verbose_name='Last 4 digits')),
                ('brand', models.CharField(blank=True, max_length=255, verbose_name='Brand of card')),
                ('exp_month', models.CharField(blank=True, max_length=255, verbose_name='Exp. month')),
                ('exp_year', models.CharField(blank=True, max_length=255, verbose_name='Exp. year')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Card holder name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
    ]
