# Generated by Django 4.2.7 on 2023-12-03 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_historical_performence_quality_rating_avg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historical_performence',
            old_name='avarage_response_time',
            new_name='average_response_time',
        ),
    ]
