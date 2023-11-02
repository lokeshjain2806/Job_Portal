from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import random
from .forms import SignUpFormRecruiter, SignUpFormSeeker, LoginForm, JobForm, JobApplicationForm, OtpLoginForm, \
    OtpVerificationForm, RegistrationForm, ContactForm, LocationForm
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication, Notification, MyUser, PostAboutModel


# Create your views here.
def Home(request):
    if request.method == 'POST':
        pass
    else:
        if request.user.is_authenticated:
            return redirect('LoginHome')
        else:
            jobs = Job.objects.all()[:4:-1]
            form = LocationForm
            about = PostAboutModel.objects.all()
            return render(request, 'base.html', {'jobs': jobs, 'form': form, 'abouts': about})


def counts(request):
    jobs_count = Job.objects.count()
    seekers_count = JobSeekerModel.objects.count()
    recruiter_count = RecruiterModel.objects.count()
    return {
        'jobs_count': jobs_count,
        'seekers_count': seekers_count,
        'recruiter_count': recruiter_count,
    }


def About(request):
    return render(request, 'about.html')


def job_list_not_auth(request, category=None):
    if category:
        jobs = Job.objects.filter(industry_category=category)[:10:-1]
    else:
        jobs = Job.objects.all()[:10:-1]
    categories = Job.INDUSTRY_CATEGORIES
    return render(request, 'job_listing_not_auth.html', {'jobs': jobs, 'categories': categories, 'selected_category': category})


@login_required(login_url="/signin/")
def LoginHome(request):
    return render(request, 'home.html')


class Registration(View):
    def get(self, request):
        form =RegistrationForm
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            a = MyUser.objects.filter(email=email).exists()
            user_name = form.cleaned_data['username']
            b = MyUser.objects.filter(username=user_name).exists()
            if a:
                messages.error(request, 'Email is already exist')
                return render(request, 'registration.html', {'form': form})
            if b:
                messages.error(request, 'username is already exist')
                return render(request, 'registration.html', {'form': form})
            user = MyUser.objects.create_user(
                username=user_name,
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
                type=form.cleaned_data['type'],
            )
            return redirect('Home')
        else:
            return render(request, 'registration.html', {'form': form})


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class SignUpSeekerView(View):
    def get(self, request):
        form = SignUpFormSeeker(initial={'email': request.user.email})
        form.fields['email'].widget.attrs['readonly'] = 'readonly'
        return render(request, 'signupseeker.html', {'form': form})

    def post(self, request):
        form = SignUpFormSeeker(request.POST, request.FILES)
        if form.is_valid():
            if 'profile_image' not in request.FILES:
                form.cleaned_data['profile_image'] = 'default_profile.png'
            seeker = JobSeekerModel(
                user=self.request.user,
                profile_image=form.cleaned_data['profile_image'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                mobile_number=form.cleaned_data['mobile_number'],
                work_experience=form.cleaned_data['work_experience'],
                resume=form.cleaned_data['resume'],
                category=form.cleaned_data['category'],
            )
            seeker.save()
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
        return redirect('LoginHome')


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class SignUpRecruiterView(View):
    def get(self, request):
        form = SignUpFormRecruiter(initial={'email_id': request.user.email})
        form.fields['email_id'].widget.attrs['readonly'] = 'readonly'
        return render(request, 'signuprecruiter.html', {'form': form})

    def post(self, request):
        form = SignUpFormRecruiter(request.POST, request.FILES)
        if form.is_valid():
            seeker = RecruiterModel(
                user=self.request.user,
                company_name=form.cleaned_data['company_name'],
                gst_no=form.cleaned_data['gst_no'],
                gst_doc=form.cleaned_data['gst_doc'],
                email_id=form.cleaned_data['email_id'],
                mobile_number=form.cleaned_data['mobile_number'],
                company_image=form.cleaned_data['company_image'],
            )
            seeker.save()
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")
        return redirect('LoginHome')


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                a = user.last_login
                login(request, user)
                if a is None:
                    if self.request.user.type == 'Is JobSeeker':
                        return redirect('SignUpSeeker')
                    else:
                        return redirect('SignUpRecruiter')
                else:
                    login(request, user)
                    return redirect('LoginHome')
            else:
                messages.error(request, 'Username Or Password is invalid')
                return render(request, 'signin.html', {'form': form})
        else:
            return render(request, 'signin.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = MyUser.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with this email does not exist.')
            return redirect('password-reset')
        return super().form_valid(form)


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class Profile(View):
    def get(self, request):
        user = request.user
        user_image = None
        user_files_resume = None
        user_files_gst = None
        form =None
        company_image = None
        if self.request.user.type == 'Is JobSeeker':
            job_seeker = JobSeekerModel.objects.filter(email=user.email).first()
            form = SignUpFormSeeker(instance=job_seeker)
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
            user_files_resume = job_seeker.resume.url
            user_image = job_seeker.profile_image.url
        else:
            job_recruiter = RecruiterModel.objects.filter(email_id=user.email).first()
            form = SignUpFormRecruiter(instance=job_recruiter)
            form.fields['email_id'].widget.attrs['readonly'] = 'readonly'
            form.fields['company_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['gst_no'].widget.attrs['readonly'] = 'readonly'
            user_files_gst = job_recruiter.gst_doc.url
            company_image = job_recruiter.company_image.url
            print(company_image)
        return render(request, 'profile.html', {'form': form, 'user_files_resume': user_files_resume, 'user_image': user_image, 'user_files_gst': user_files_gst, 'company_image': company_image})

    def post(self, request):
        user = request.user
        user_image = None
        if self.request.user.type == 'Is JobSeeker':
            job_seeker = JobSeekerModel.objects.filter(email=user.email).first()
            form = SignUpFormSeeker(request.POST, request.FILES, instance=job_seeker)
            if form.is_valid():
                seeker = JobSeekerModel.objects.get(user=user)
                seeker.user = user
                seeker.name = form.cleaned_data['name']
                seeker.email = form.cleaned_data['email']
                seeker.mobile_number = form.cleaned_data['mobile_number']
                seeker.work_experience = form.cleaned_data['work_experience']
                seeker.resume = form.cleaned_data['resume']
                seeker.profile_image = form.cleaned_data['profile_image']
                seeker.category = form.cleaned_data['category']
                seeker.save()
                return redirect('LoginHome')
            else:
                return render(request, 'profile.html', {'form': form})
        else:
            job_recruiter = RecruiterModel.objects.filter(email_id=user.email).first()
            form = SignUpFormRecruiter(request.POST, request.FILES, instance=job_recruiter)
            if form.is_valid():
                recruiter = RecruiterModel.objects.get(user=user)
                recruiter.user = user
                recruiter.company_name = form.cleaned_data['company_name']
                recruiter.email_id = form.cleaned_data['email_id']
                recruiter.gst_no = form.cleaned_data['gst_no']
                recruiter.gst_doc = form.cleaned_data['gst_doc']
                recruiter.mobile_number = form.cleaned_data['mobile_number']
                recruiter.save()
                return redirect('LoginHome')
            else:
                return render(request, 'profile.html', {'form': form})


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('Home')


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_posting_form.html'
    success_url = reverse_lazy('user-jobs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        job = Job.objects.filter(user=self.request.user).first()
        recuiter = self.request.user.job_recruiter
        recruiter_profile = self.request.user.job_recruiter
        company_name = recruiter_profile.company_name
        company_image = recruiter_profile.company_image
        form.instance.company_name = company_name
        form.instance.company_image = company_image
        form.instance.recuiter = recuiter
        form.save()
        job_seekers = JobSeekerModel.objects.all()
        for job_seeker in job_seekers:
            notification = Notification.objects.create(
                user=job_seeker.user,
                job=form.instance,
                notify="New Job Alert",
            )
        return super().form_valid(form)


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class UserJobListView(ListView):
    model = Job
    template_name = 'user_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user).order_by('-id')


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
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


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class JobDeleteView(DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('user-jobs')


@login_required(login_url="/signin/")
def ShowAllJobs(request):
    jobs = Job.objects.all()
    user = request.user
    applied_jobs = set(job_app.job.id for job_app in JobApplication.objects.filter(job_seeker__user=user))
    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
    }

    return render(request, 'showalljobs.html', context)


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
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
        initial['phone_number'] = seeker.mobile_number
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


@login_required(login_url="/signin/")
def JobApplicationsListView(request):
    if request.user.is_authenticated:
        job_seeker = request.user.job_seeker
        applications = JobApplication.objects.filter(job_seeker=job_seeker)
    return render(request, 'job_applications_list.html', {'applications': applications})


@login_required(login_url="/signin/")
def job_applications_view_admin(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})


@login_required(login_url="/signin/")
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
            email = form.cleaned_data['email_id']
            a = MyUser.objects.filter(email=email).exists()
            if a:
                num_numbers = 6
                random_numbers = []
                for i in range(num_numbers):
                    random_1_digit = random.randint(1, 9)
                    random_numbers.append(str(random_1_digit))
                otp = int(''.join(random_numbers))
                request.session['email'] = email
                request.session['expected_otp'] = otp
                request.session.save()
                subject = 'Login Verification'
                message = f'Otp For Login: {otp}. Otp is valid for 10 minutes only.'
                from_email = 'reset9546@gmail.com'
                recipient_list = [email]
                fail_silently = False
                send_mail(subject, message, from_email, recipient_list, fail_silently)
                return redirect('OtpVerification')
            else:
                messages.error(request, 'Email id Does Not Exist')
                return render(request, 'otplogin.html',  {'form': form})


class OtpVerification(View):
    def get(self, request):
        form = OtpVerificationForm
        return render(request, 'otpverification.html', {'form': form})

    def post(self, request):
        form = OtpVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = request.POST.get('otp')
            expected_otp = request.session.get('expected_otp')
            email = request.session.get('email')
            user = MyUser.objects.get(email=email)
            if str(entered_otp) == str(expected_otp):
                login(request, user)
                return redirect('LoginHome')
            else:
                messages.error(request, 'Please Enter Valid Otp')
                return render(request, 'otpverification.html', {'form': form})


@method_decorator(login_required(login_url="/signin/"), name='dispatch')
class NotificationView(View):
    def get(self, request):
        user = self.request.user
        job_seeker = get_object_or_404(JobSeekerModel, user=user)
        category = job_seeker.category
        notifications = Notification.objects.filter(user=user).order_by('-id')
        if category:
            notifications = notifications.filter(job__industry_category=category)
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


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            subject = 'New Contact Form Submission'
            message = f'Name: {contact.name}\nEmail: {contact.email}\nSubject: {contact.subject}\nMessage: {contact.message}'
            from_email = 'reset9546@gmail.com'
            recipient_list = ['lokeshjain2806@gmail.com']
            send_mail(subject, message, from_email, recipient_list)

            return redirect('Home')

        return render(request, self.template_name, {'form': form})


def search_with_location(request):
    query = request.GET.get('job_title')
    query1 = request.GET.get('location')
    if query and not query1:
        data = Job.objects.filter(Q(job_title__icontains=query))
    elif not query and query1:
        data = Job.objects.filter(Q(location__icontains=query1))
    elif query and query1:
        data = Job.objects.filter(Q(job_title__icontains=query) & Q(location__icontains=query1))
    else:
        data = Job.objects.all()
    return render(request, 'search_with_location.html', {'data': data})

