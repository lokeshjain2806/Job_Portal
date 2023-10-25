from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import random
from .forms import SignUpFormRecruiter, SignUpFormSeeker, LoginForm, JobForm, JobApplicationForm, OtpLoginForm, \
    OtpVerificationForm
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication, Notification


# Create your views here.
def Home(request):
    if request.user.is_authenticated:
        return redirect('LoginHome')
    else:
        jobs = Job.objects.all()[:10]
        return render(request, 'base.html', {'jobs': jobs})


def About(request):
    return render(request, 'about.html')


def LoginHome(request):
    return render(request, 'home.html')


class SignUpSeekerView(View):
    def get(self, request):
        form = SignUpFormSeeker
        return render(request, 'signupseeker.html', {'form': form})

    def post(self, request):
        form = SignUpFormSeeker(request.POST, request.FILES)
        if form.is_valid():
            user_name = form.cleaned_data['email']
            a = User.objects.filter(username=user_name).exists()
            if a:
                messages.error(request, 'username is already exist')
                return render(request, 'signupseeker.html', {'form': form})
            else:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Please Enter Same Password')
                    return render(request, 'signupseeker.html', {'form': form})
                if 'profile_image' not in request.FILES:
                    form.cleaned_data['profile_image'] = 'default_profile.png'
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    password=password1,
                    email=form.cleaned_data['email'],
                )
                seeker = JobSeekerModel(
                    user=user,
                    profile_image=form.cleaned_data['profile_image'],
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    mobile_number=form.cleaned_data['mobile_number'],
                    work_experience=form.cleaned_data['work_experience'],
                    resume=form.cleaned_data['resume'],
                )
                seeker.save()
                permission = Permission.objects.get(codename='can_view_job_seekers_custom')
                user.user_permissions.add(permission)
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
        return redirect('Login')


class SignUpRecruiterView(View):
    def get(self, request):
        form = SignUpFormRecruiter
        return render(request, 'signuprecruiter.html', {'form': form})

    def post(self, request):
        form = SignUpFormRecruiter(request.POST, request.FILES)
        if form.is_valid():
            user_name = form.cleaned_data['email_id']
            a = User.objects.filter(username=user_name).exists()
            if a:
                messages.error(request, 'username is already exist')
                return render(request, 'signupseeker.html', {'form': form})
            else:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Password Not Match')
                    return render(request, 'signupseeker.html', {'form': form})
                user = User.objects.create_user(
                    username=form.cleaned_data['email_id'],
                    password=password1,
                    email=form.cleaned_data['email_id'],
                )
                seeker = RecruiterModel(
                    user=user,
                    company_name=form.cleaned_data['company_name'],
                    gst_no=form.cleaned_data['gst_no'],
                    gst_doc=form.cleaned_data['gst_doc'],
                    email_id=form.cleaned_data['email_id'],
                    mobile_number=form.cleaned_data['mobile_number'],
                )
                seeker.save()
                permission = Permission.objects.get(codename='can_view_recruiter_custom')
                user.user_permissions.add(permission)
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
        return redirect('Login')


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'signin.html', {'form': form})

    def post(self,request):
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email_id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('LoginHome')
            else:
                messages.error(request, 'Please Enter Valid Email Id And Password')
                return render(request, 'signin.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with this email does not exist.')
            return redirect('password-reset')
        return super().form_valid(form)


class Profile(View):
    def get(self, request):
        user = request.user
        user_image = None
        user_files_resume = None
        user_files_gst = None
        form =None
        if user.has_perm('app.can_view_job_seekers_custom'):
            job_seeker = JobSeekerModel.objects.filter(email=user).first()
            form = SignUpFormSeeker(instance=job_seeker)
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
            user_files_resume = job_seeker.resume
            user_image = job_seeker.profile_image.url
        elif user.has_perm('app.can_view_recruiter_custom'):
            job_recruiter = RecruiterModel.objects.filter(email_id=user.email).first()
            form = SignUpFormRecruiter(instance=job_recruiter)
            form.fields['email_id'].widget.attrs['readonly'] = 'readonly'
            form.fields['company_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['gst_no'].widget.attrs['readonly'] = 'readonly'
            user_files_gst = job_recruiter.gst_doc
        return render(request, 'profile.html', {'form': form, 'user_files_resume': user_files_resume, 'user_image': user_image, 'user_files_gst': user_files_gst})

    def post(self, request):
        user = request.user
        user_image = None
        if user.has_perm('app.can_view_job_seekers_custom'):
            job_seeker = JobSeekerModel.objects.filter(email=user.email).first()
            form = SignUpFormSeeker(request.POST, request.FILES, instance=job_seeker)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Passwords Do Not Match')
                    return render(request, 'profile.html', {'form': form})
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']

                seeker = JobSeekerModel.objects.get(user=user)
                seeker.user = user
                seeker.name = form.cleaned_data['name']
                seeker.email = email
                seeker.mobile_number = form.cleaned_data['mobile_number']
                seeker.work_experience = form.cleaned_data['work_experience']
                seeker.email_id = email
                seeker.resume = form.cleaned_data['resume']
                seeker.profile_image = form.cleaned_data['profile_image']
                seeker.save()

                user.set_password(password)
                user.save()
                updated_user = authenticate(username=user.username, password=password1)
                if updated_user is not None:
                    login(request, updated_user)
                return redirect('LoginHome')
            else:
                messages.error(request, 'Password Is Not Match')
                return render(request, 'profile.html', {'form': form})
        elif user.has_perm('app.can_view_recruiter_custom'):
            job_recruiter = RecruiterModel.objects.filter(email_id=user.email).first()
            form = SignUpFormRecruiter(request.POST, request.FILES, instance=job_recruiter)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    messages.error(request, 'Passwords Do Not Match')
                    return render(request, 'profile.html', {'form': form})
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email_id']

                recruiter = RecruiterModel.objects.get(user=user)
                recruiter.user = user
                recruiter.company_name = form.cleaned_data['company_name']
                recruiter.email_id = email
                recruiter.gst_no = form.cleaned_data['gst_no']
                recruiter.gst_doc = form.cleaned_data['gst_doc']
                recruiter.mobile_number = form.cleaned_data['mobile_number']
                recruiter.save()

                user.set_password(password)
                user.save()
                updated_user = authenticate(username=user.username, password=password1)
                if updated_user is not None:
                    login(request, updated_user)
                return redirect('LoginHome')
            else:
                messages.error(request, 'Password Is Not Match')
                return render(request, 'profile.html', {'form': form})



class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('Home')


class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_posting_form.html'
    success_url = reverse_lazy('user-jobs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        job = Job.objects.filter(user=self.request.user).first()
        recruiter_profile = self.request.user.job_recruiter
        company_name = recruiter_profile.company_name
        form.instance.company_name = company_name
        form.save()
        job_seekers = JobSeekerModel.objects.all()
        for job_seeker in job_seekers:
            notification = Notification.objects.create(
                user=job_seeker.user,
                job=job,
                notify="New Job Alert",
            )
        return super().form_valid(form)


class UserJobListView(ListView):
    model = Job
    template_name = 'user_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user).order_by('-id')


class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job_edit.html'
    success_url = reverse_lazy('user-jobs')

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super(JobUpdateView, self).get_form(form_class)
        return form


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('user-jobs')


def ShowAllJobs(request):
    jobs = Job.objects.all()
    user = request.user
    applied_jobs = set(job_app.job.id for job_app in JobApplication.objects.filter(job_seeker__user=user))
    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
    }

    return render(request, 'showalljobs.html', context)


class JobApplicationCreateView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job_application_form.html'
    success_url = reverse_lazy('job-applications-list')

    def get_initial(self):
        initial = super().get_initial()
        seeker = self.request.user.job_seeker
        initial['email'] = seeker.email
        initial['full_name'] = seeker.name
        return initial

    def form_valid(self, form):
        job_seeker = self.request.user.job_seeker
        form.instance.job_seeker = job_seeker
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Job, pk=job_id)
        form.instance.job = job
        form.save()
        subject = 'Job Application Confirmation'
        message = f'Your job application for the following job has been submitted successfully:\n\n'
        message += f'Job Title: {job.job_title}\n'
        message += f'Company Name: {job.company_name}\n'
        message += f'Location: {job.location}\n'
        message += f'Job Type: {job.get_job_type_display()}\n'
        message += f'Industry Category: {job.get_industry_category_display()}\n'
        message += f'Salary: Rs. {job.salary}\n'
        message += f'Job Requirements: {job.job_requirements}\n'
        message += f'Education Requirements: {job.education_requirements}\n'
        message += f'Experience Level: {job.experience_level}\n'
        message += f'Contact Information: {job.contact_information}\n'
        message += f'Benefits: {job.benefits}\n'
        message += f'Skills and Qualities: {job.skills_and_qualities}\n'
        from_email = 'reset9546@gmail.com'
        recipient_list = [job_seeker.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return super().form_valid(form)


def JobApplicationsListView(request):
    if request.user.is_authenticated:
        job_seeker = request.user.job_seeker
        applications = JobApplication.objects.filter(job_seeker=job_seeker)
    return render(request, 'job_applications_list.html', {'applications': applications})


def job_applications_view_admin(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})


def search(request):
    query = request.GET.get('job_title')
    data = Job.objects.filter(job_title__icontains=query)
    user = request.user
    applied_jobs = set(job_app.job.id for job_app in JobApplication.objects.filter(job_seeker__user=user))
    return render(request, 'searchjobs.html', {'data': data, 'query': query, 'applied_jobs': applied_jobs})


class LoginViaOtpView(View):
    def get(self, request):
        form = OtpLoginForm
        return render(request, 'otplogin.html',  {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['email_id']
            a = User.objects.filter(username=user_name).exists()
            if a:
                num_numbers = 6
                random_numbers = []
                for i in range(num_numbers):
                    random_1_digit = random.randint(1, 9)
                    random_numbers.append(str(random_1_digit))
                otp = int(''.join(random_numbers))
                request.session['email_id'] = user_name
                request.session['expected_otp'] = otp
                request.session.save()
                subject = 'Login Verification'
                message = f'Otp For Login: {otp}. Otp is valid for 10 minutes only.'
                from_email = 'reset9546@gmail.com'
                recipient_list = [user_name]
                fail_silently = False
                send_mail(subject, message, from_email, recipient_list, fail_silently)
                return redirect('OtpVerification')
            else:
                pass


class OtpVerification(View):
    def get(self, request):
        form = OtpVerificationForm
        return render(request, 'otpverification.html', {'form': form})

    def post(self, request):
        form = OtpVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = request.POST.get('otp')
            expected_otp = request.session.get('expected_otp')
            user_email = request.session.get('email_id')
            user = User.objects.get(username=user_email)
            if str(entered_otp) == str(expected_otp):
                login(request, user)
                return redirect('LoginHome')
            else:
                return render(request, 'otpverification.html', {'form': form})


class NotificationView(View):
    def get(self, request):
        user = self.request.user
        notifications = Notification.objects.filter(user=user)
        notify_count = notifications.count()
        context = {
            'notifications': notifications,
            'notify_count': notify_count,
        }
        return render(request, 'notification.html', context)


class JobDetailView(View):
    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        context = {
            'job': job,
        }
        return render(request, 'job_details.html', context)
