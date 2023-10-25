from django.contrib import admin
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication

admin.site.register(JobSeekerModel)
admin.site.register(RecruiterModel)
admin.site.register(Job)
admin.site.register(JobApplication)