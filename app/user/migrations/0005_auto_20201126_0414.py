# Generated by Django 3.1.2 on 2020-11-26 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0004_auto_20201126_0414'),
        ('user', '0004_favouriteclass_favouritecreator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorreview',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('card_number', models.CharField(blank=True, max_length=19, null=True)),
                ('expiry_month_year', models.CharField(blank=True, max_length=7, null=True)),
                ('stripe_token', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_credit_card_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Card Detail',
                'verbose_name_plural': 'User Card Details',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StreamBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_stream', to='creator.stream')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream_booking_by', to=settings.AUTH_USER_MODEL)),
                ('user_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_stream_payment', to='user.usercard')),
            ],
            options={
                'verbose_name': 'Stream booking',
                'verbose_name_plural': 'Stream bookings',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SessionBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_with', to='creator.creator')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_slot', to='creator.timeslot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_by', to=settings.AUTH_USER_MODEL)),
                ('user_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_session_payment', to='user.usercard')),
            ],
            options={
                'verbose_name': 'Session booking',
                'verbose_name_plural': 'Session bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]
