# Generated by Django 3.1.2 on 2021-06-16 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0031_auto_20210603_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorclass',
            name='class_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
