# Generated by Django 3.1.2 on 2021-06-02 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0012_auto_20210504_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=222, null=True),
        ),
    ]
