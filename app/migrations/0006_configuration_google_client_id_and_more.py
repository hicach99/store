# Generated by Django 4.1.7 on 2023-03-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_configuration_address_ar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='google_client_id',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='configuration',
            name='google_client_secret',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]