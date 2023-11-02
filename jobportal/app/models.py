from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    REGISTRATION_CHOICES = [
        ('Is JobSeeker', 'Is JobSeeker'),
        ('Is JobRecruiter', 'Is JobRecruiter'),
    ]
    type = models.CharField(max_length=20, choices=REGISTRATION_CHOICES)


class JobSeekerModel(models.Model):
    WORK_EXPERIENCE_CHOICES = [
        ('Fresher', 'Fresher'),
        ('Experienced', 'Experienced'),
    ]
    INDUSTRY_CATEGORIES = [
        ('Information Technology', 'Information Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Design & Creative', 'Design & Creative'),
        ('Design & Development', 'Design & Development'),
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Mobile Application', 'Mobile Application'),
        ('Construction', 'Construction'),
        ('Real Estate', 'Real Estate'),
        ('Content Writer', 'Content Writer'),
        ('Textile', 'Textile'),
        ('Media and news', 'Media and news'),
        ('Food processing', 'Food processing'),
        ('Law', 'Law'),
        ('Advertising', 'Advertising'),
    ]
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='job_seeker')
    profile_image = models.ImageField(upload_to='profile_images/', verbose_name='Profile Image', default='default_profile.png')
    name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email Id', unique=True)
    mobile_number = models.BigIntegerField(verbose_name='Mobile Number')
    work_experience = models.CharField(max_length=20, choices=WORK_EXPERIENCE_CHOICES, verbose_name='Work Experience')
    resume = models.FileField(upload_to='resumes/', verbose_name='Resume')
    category = models.CharField(max_length=50, choices=INDUSTRY_CATEGORIES, default='IT', null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Job Seeker'
        verbose_name_plural = 'Job Seekers'
        permissions = [
            ("can_view_job_seekers_custom", "Can View Job Seekers Custom"),
        ]


class RecruiterModel(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='job_recruiter')
    company_image = models.ImageField(upload_to='company_images/', verbose_name='Company Image')
    company_name = models.CharField(max_length=100, verbose_name='Company Full Name')
    gst_no = models.CharField(max_length=15, verbose_name='GSTIN Number')
    gst_doc = models.FileField(upload_to='gst_documents/', verbose_name='Upload GST Document')
    email_id = models.EmailField(verbose_name='Email Id', unique=True)
    mobile_number = models.BigIntegerField(verbose_name='Mobile Number')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Recruiter'
        verbose_name_plural = 'Recruiters'
        permissions = [
            ("can_view_recruiter_custom", "Can View Recruiter Custom"),
        ]


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('other', 'Other'),
    ]
    INDUSTRY_CATEGORIES = [
        ('Information Technology', 'Information Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Design & Creative', 'Design & Creative'),
        ('Design & Development', 'Design & Development'),
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Mobile Application', 'Mobile Application'),
        ('Construction', 'Construction'),
        ('Real Estate', 'Real Estate'),
        ('Content Writer', 'Content Writer'),
        ('Textile', 'Textile'),
        ('Media and news', 'Media and news'),
        ('Food processing', 'Food processing'),
        ('Law', 'Law'),
        ('Advertising', 'Advertising'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(JobSeekerModel, related_name="applied_jobs", blank=True)
    recuiter = models.ForeignKey(RecruiterModel, related_name='recuiter', null=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    company_name = models.CharField(max_length=100)
    company_image = models.ImageField(upload_to='company_images/', verbose_name='Company Image', null=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    industry_category = models.CharField(
        max_length=50,
        choices=INDUSTRY_CATEGORIES,
        default='IT'
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_requirements = models.TextField()
    education_requirements = models.CharField(max_length=50)
    experience_level = models.CharField(max_length=20)
    contact_information = models.CharField(max_length=100)
    benefits = models.TextField()
    skills_and_qualities = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    job_seeker = models.ForeignKey(JobSeekerModel, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.full_name


class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    notify = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.notify


class ContactModel(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class PostAboutModel(models.Model):
    image = models.ImageField(upload_to='about_images/', verbose_name='About Image')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=255)
    about = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)


class Location(models.Model):
    location_name = models.CharField(max_length=255, null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.location_name
