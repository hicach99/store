# Generated by Django 4.1.7 on 2023-03-22 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_banner_bannerimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='description_ar',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='description_en',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='description_fr',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_ar',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_en',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_fr',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
