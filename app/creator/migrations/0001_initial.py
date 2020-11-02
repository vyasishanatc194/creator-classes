# Generated by Django 3.1.2 on 2020-11-02 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.user')),
                ('key_skill', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('instagram_url', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('linkedin_url', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('twitter_url', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('google_url', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('facebook_url', models.CharField(blank=True, default='', max_length=40, null=True)),
            ],
            options={
                'verbose_name': 'Creator',
                'verbose_name_plural': 'Creators',
                'ordering': ['-created_at'],
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='CreatorSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('skill', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='creator.creator')),
            ],
            options={
                'verbose_name': 'Creator skill',
                'verbose_name_plural': 'Creator skills',
                'ordering': ['-created_at'],
            },
        ),
    ]
