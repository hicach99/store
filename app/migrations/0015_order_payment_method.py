# Generated by Django 4.1.7 on 2023-03-17 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_configuration_logo_configuration_logo_white_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
