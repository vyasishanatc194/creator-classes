# Generated by Django 3.1.2 on 2020-12-23 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_sessionbooking_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionbooking',
            name='keywords',
        ),
    ]
