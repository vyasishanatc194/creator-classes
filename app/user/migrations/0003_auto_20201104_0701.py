# Generated by Django 3.1.2 on 2020-11-04 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0002_classcovers_classkeyword_creatorclass'),
        ('user', '0002_auto_20201103_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='sample.jpg', null=True, upload_to='profile_image', verbose_name='Profile Image'),
        ),
        migrations.CreateModel(
            name='ClassReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date when created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date when updated.', null=True, verbose_name='Updated At')),
                ('review', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('rating', models.FloatField(blank=True, default=1, null=True)),
                ('creator_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_for_class', to='creator.creatorclass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_review_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Class Review',
                'verbose_name_plural': 'Class reviews',
                'ordering': ['-created_at'],
            },
        ),
    ]
