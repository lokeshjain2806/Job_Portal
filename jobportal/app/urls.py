from django.urls import path
from .views import Home, SignUpSeekerView, SignUpRecruiterView, Login, CustomPasswordResetView, Profile, LoginHome, \
    UserLogout, JobCreateView, UserJobListView, JobUpdateView, JobDeleteView, ShowAllJobs, JobApplicationCreateView, \
    JobApplicationsListView, job_applications_view_admin, search, LoginViaOtpView, OtpVerification, About, \
    NotificationView, JobDetailView
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', Home, name='Home'),
    path('about/', About, name='About'),
    path('home/', LoginHome, name='LoginHome'),
    path('signupseeker/', SignUpSeekerView.as_view(), name='SignUpSeeker'),
    path('signuprecruiter/', SignUpRecruiterView.as_view(), name='SignUpRecruiter'),
    path('signin', Login.as_view(), name='Login'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='resetpassword.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')),
    path('home/profile/', Profile.as_view(), name='Profile'),
    path('home/notifications/', NotificationView.as_view(), name='Notifications'),
    path('home/add/', JobCreateView.as_view(), name='create-job'),
    path('home/user_jobs/', UserJobListView.as_view(), name='user-jobs'),
    path('home/edit_job/<int:pk>/', JobUpdateView.as_view(), name='edit-job'),
    path('home/logout/', UserLogout.as_view(), name='Logout'),
    path('home/job/<int:pk>/delete/', JobDeleteView.as_view(), name='delete-job'),
    path('home/showjobs/', ShowAllJobs, name='show-jobs'),
    path('home/job/apply/<int:job_id>/', JobApplicationCreateView.as_view(), name='JobApplicationCreateView'),
    path('home/job/applications/', JobApplicationsListView, name='job-applications-list'),
    path('home/job/applications/<int:job_id>/', job_applications_view_admin, name='job-applications'),
    path('home/search/', search, name='search'),
    path('otplogin/', LoginViaOtpView.as_view(), name='LoginViaOtp'),
    path('otplogin/otpverification/', OtpVerification.as_view(), name='OtpVerification'),
    path('home/job_details/<int:job_id>/', JobDetailView.as_view(), name='JobDetail'),


]
