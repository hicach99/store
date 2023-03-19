# Generated by Django 4.1.7 on 2023-03-18 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_order_options_configuration_favicon_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name_plural': 'Properties'},
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_public_key',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_sandbox',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_secret_key',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
