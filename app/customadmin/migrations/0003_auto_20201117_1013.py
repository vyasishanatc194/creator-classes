# Generated by Django 3.1.2 on 2020-11-17 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0002_auto_20201117_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='duration_in_months',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
