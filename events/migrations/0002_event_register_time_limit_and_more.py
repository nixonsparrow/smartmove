# Generated by Django 4.0.3 on 2022-03-26 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='register_time_limit',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Register time limit (minutes)'),
        ),
        migrations.AddField(
            model_name='event',
            name='unregister_time_limit',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Unregister time limit (minutes)'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='direction',
            field=models.SmallIntegerField(choices=[(1, 'In'), (-1, 'Out')], default=(1, 'In'), verbose_name='Registering'),
        ),
    ]
