# Generated by Django 4.1.7 on 2023-03-22 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_customer_name_alter_customer_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_color', models.CharField(blank=True, max_length=254)),
                ('background_image', models.ImageField(blank=True, upload_to='banner_images/')),
                ('title', models.CharField(blank=True, max_length=254)),
                ('title_color', models.CharField(blank=True, max_length=254)),
                ('description', models.CharField(blank=True, max_length=254)),
                ('description_color', models.CharField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BannerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='banner_images/')),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.banner')),
            ],
        ),
    ]
