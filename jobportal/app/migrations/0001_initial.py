# Generated by Django 4.2.6 on 2023-10-27 04:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('type', models.CharField(choices=[('JobSeeker', 'JobSeeker'), ('JobRecruiter', 'JobRecruiter')], max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('job_description', models.TextField()),
                ('company_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('freelance', 'Freelance'), ('internship', 'Internship'), ('other', 'Other')], max_length=20)),
                ('industry_category', models.CharField(choices=[('IT', 'Information Technology'), ('Healthcare', 'Healthcare'), ('Finance', 'Finance'), ('Education', 'Education')], default='IT', max_length=50)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('job_requirements', models.TextField()),
                ('education_requirements', models.CharField(max_length=50)),
                ('experience_level', models.CharField(max_length=20)),
                ('contact_information', models.CharField(max_length=100)),
                ('benefits', models.TextField()),
                ('skills_and_qualities', models.TextField()),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecruiterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_image', models.ImageField(upload_to='company_images/', verbose_name='Company Image')),
                ('company_name', models.CharField(max_length=100, verbose_name='Company Full Name')),
                ('gst_no', models.CharField(max_length=15, verbose_name='GSTIN Number')),
                ('gst_doc', models.FileField(upload_to='gst_documents/', verbose_name='Upload GST Document')),
                ('email_id', models.EmailField(max_length=254, unique=True, verbose_name='Email Id')),
                ('mobile_number', models.BigIntegerField(verbose_name='Mobile Number')),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_recruiter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recruiter',
                'verbose_name_plural': 'Recruiters',
                'permissions': [('can_view_recruiter_custom', 'Can View Recruiter Custom')],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify', models.TextField()),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='default_profile.png', upload_to='profile_images/', verbose_name='Profile Image')),
                ('name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Id')),
                ('mobile_number', models.BigIntegerField(verbose_name='Mobile Number')),
                ('work_experience', models.CharField(choices=[('Fresher', 'Fresher'), ('Experienced', 'Experienced')], max_length=20, verbose_name='Work Experience')),
                ('resume', models.FileField(upload_to='resumes/', verbose_name='Resume')),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Seeker',
                'verbose_name_plural': 'Job Seekers',
                'permissions': [('can_view_job_seekers_custom', 'Can View Job Seekers Custom')],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='app.job')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.jobseekermodel')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='applied_jobs', to='app.jobseekermodel'),
        ),
        migrations.AddField(
            model_name='job',
            name='recuiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recuiter', to='app.recruitermodel'),
        ),
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
