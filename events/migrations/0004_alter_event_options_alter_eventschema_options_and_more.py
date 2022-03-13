# Generated by Django 4.0.3 on 2022-03-13 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_participants_event_time_event_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='eventschema',
            options={'verbose_name': 'Event schema', 'verbose_name_plural': 'Events schemas'},
        ),
        migrations.AddField(
            model_name='event',
            name='participants_limit',
            field=models.IntegerField(default=10, verbose_name='Limit of participants'),
        ),
        migrations.AddField(
            model_name='eventschema',
            name='participants_limit',
            field=models.IntegerField(default=10, verbose_name='Limit of participants'),
        ),
        migrations.AlterField(
            model_name='event',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.eventschema', verbose_name='Schema'),
        ),
    ]
