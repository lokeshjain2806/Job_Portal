# Generated by Django 4.2.6 on 2023-10-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekermodel',
            name='profile_image',
            field=models.ImageField(default='/static/images/default-profile.png', upload_to='profile_images/', verbose_name='Profile Image'),
        ),
    ]
