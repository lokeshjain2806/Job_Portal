# Generated by Django 4.2.6 on 2023-10-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='about_images/', verbose_name='About Image')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=255)),
                ('about', models.TextField()),
            ],
        ),
    ]