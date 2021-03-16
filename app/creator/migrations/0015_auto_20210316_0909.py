# Generated by Django 3.1.2 on 2021-03-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0014_auto_20210215_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='agora_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='agora_uid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='channel_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stream',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='agora_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='agora_uid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='channel_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
