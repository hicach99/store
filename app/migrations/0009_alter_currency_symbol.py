# Generated by Django 4.1.7 on 2023-03-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_configuration_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
