# Generated by Django 4.0.3 on 2022-03-10 23:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]