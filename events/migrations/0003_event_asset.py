# Generated by Django 5.2.3 on 2025-07-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_attendees_alter_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, null=True, upload_to='event_asset'),
        ),
    ]
