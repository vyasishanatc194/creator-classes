# Generated by Django 3.1.2 on 2021-04-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0019_stream_screen_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorclass',
            name='class_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
