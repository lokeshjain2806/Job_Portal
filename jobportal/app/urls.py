from django.urls import path

from .forms import CustomPasswordResetConfirmForm
from .views import Home, job_list_not_auth, ContactView, Registration, About, Login, LoginHome, UserLogout, \
    LoginViaOtpView, OtpVerification, CustomPasswordResetView, JobCreateView, UserJobListView, JobUpdateView, \
    JobDeleteView, job_applications_view_admin, ShowAllJobs, JobDetailView, search, JobApplicationCreateView, \
    JobApplicationsListView, SignUpSeekerView, SignUpRecruiterView, Profile, NotificationView, search_with_location
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', Home, name='Home'),
    path('jobs/', job_list_not_auth, name='job_list_not_auth'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('registration/', Registration.as_view(), name='Registration'),
    path('about/', About, name='About'),
    path('home/', LoginHome, name='LoginHome'),
    path('updateseekerprofile/', SignUpSeekerView.as_view(), name='SignUpSeeker'),
    path('signuprecruiter/', SignUpRecruiterView.as_view(), name='SignUpRecruiter'),
    path('signin/', Login.as_view(), name='Login'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='resetpassword.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=CustomPasswordResetConfirmForm),
         name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('home/profile/', Profile.as_view(), name='Profile'),
    path('home/notifications/', NotificationView.as_view(), name='Notification'),
    path('home/add/', JobCreateView.as_view(), name='create-job'),
    path('home/jobs/', UserJobListView.as_view(), name='user-jobs'),
    path('home/job/<int:pk>/', JobUpdateView.as_view(), name='edit-job'),
    path('home/job/<int:pk>/delete/', JobDeleteView.as_view(), name='delete-job'),
    path('home/job/applications/<int:job_id>/', job_applications_view_admin, name='job-applications'),
    path('home/logout/', UserLogout.as_view(), name='Logout'),
    path('home/showjobs/', ShowAllJobs, name='show-jobs'),
    path('home/job/apply/<int:job_id>/', JobApplicationCreateView.as_view(), name='JobApplicationCreateView'),
    path('home/job/applications/', JobApplicationsListView, name='job-applications-list'),
    path('home/search/', search, name='search'),
    path('otplogin/', LoginViaOtpView.as_view(), name='LoginViaOtp'),
    path('otplogin/otpverification/', OtpVerification.as_view(), name='OtpVerification'),
    path('home/job_details/<int:job_id>/', JobDetailView.as_view(), name='JobDetail'),
    path('searchjob/', search_with_location, name='search_with_location'),
]
