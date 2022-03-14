# Generated by Django 4.0.3 on 2022-03-13 21:39

import datetime

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events_as_participant', to=settings.AUTH_USER_MODEL, verbose_name='Participants'),
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(default=datetime.time(18, 0), verbose_name='Time'),
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='', max_length=50, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='event',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_as_trainer', to=settings.AUTH_USER_MODEL, verbose_name='Trainer'),
        ),
        migrations.CreateModel(
            name='EventSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50, verbose_name='Title')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=None, verbose_name='Weekday')),
                ('time', models.TimeField(default=datetime.time(18, 0), verbose_name='Time')),
                ('date_from', models.DateField(default=django.utils.timezone.now, verbose_name='Date from')),
                ('date_to', models.DateField(default=django.utils.timezone.now, verbose_name='Date to')),
                ('type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.type')),
            ],
        ),
    ]
