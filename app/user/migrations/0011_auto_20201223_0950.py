# Generated by Django 3.1.2 on 2020-12-23 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0001_initial'),
        ('user', '0010_auto_20201223_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionbooking',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='BookedSessionKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('keyword', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customadmin.adminkeyword')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_slot', to='user.sessionbooking')),
            ],
            options={
                'verbose_name': 'Session booking keyword',
                'verbose_name_plural': 'Session booking keywords',
                'ordering': ['-created_at'],
            },
        ),
    ]
