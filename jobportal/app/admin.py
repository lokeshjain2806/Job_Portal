from django.contrib import admin
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication, MyUser, Location, ContactModel, Notification, PostAboutModel

admin.site.register(JobSeekerModel)
admin.site.register(RecruiterModel)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(MyUser)
admin.site.register(Location)
admin.site.register(ContactModel)
admin.site.register(Notification)
admin.site.register(PostAboutModel)
