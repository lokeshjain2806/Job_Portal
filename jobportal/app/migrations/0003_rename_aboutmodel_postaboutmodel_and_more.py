# Generated by Django 4.2.6 on 2023-10-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_aboutmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AboutModel',
            new_name='PostAboutModel',
        ),
        migrations.AlterField(
            model_name='job',
            name='industry_category',
            field=models.CharField(choices=[('Information Technology', 'Information Technology'), ('Healthcare', 'Healthcare'), ('Finance', 'Finance'), ('Education', 'Education'), ('Design & Creative', 'Design & Creative'), ('Design & Development', 'Design & Development'), ('Sales & Marketing', 'Sales & Marketing'), ('Mobile Application', 'Mobile Application'), ('Construction', 'Construction'), ('Real Estate', 'Real Estate'), ('Content Writer', 'Content Writer'), ('Textile', 'Textile'), ('Media and news', 'Media and news'), ('Food processing', 'Food processing'), ('Law', 'Law'), ('Advertising', 'Advertising')], default='IT', max_length=50),
        ),
    ]
