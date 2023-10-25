from django import forms
from django.contrib.auth.models import User
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication


class SignUpFormSeeker(forms.ModelForm):
    name = forms.CharField(label='Full Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
    email = forms.EmailField(label='Email Id',
                           widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True
                           )
    mobile_number = forms.IntegerField(label='Mobile Number',
                                       widget=forms.TextInput(attrs={'class': 'form-control'})
                                       )
    work_experience = forms.ChoiceField(
        label='Work Experience',
        choices=JobSeekerModel.WORK_EXPERIENCE_CHOICES, widget=forms.Select(attrs={'class': 'form-control work-experience-label'}),
    )
    resume = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)
    password1 = forms.CharField(label='Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                       )
    password2 = forms.CharField(label='Confirm Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)

    class Meta:
        model = JobSeekerModel
        fields = ['profile_image', 'name', 'email', 'mobile_number', 'work_experience', 'resume', 'password1', 'password2']


class SignUpFormRecruiter(forms.ModelForm):
    company_name = forms.CharField(
        label='Company Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gst_no = forms.CharField(
        label='GSTIN Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gst_doc = forms.FileField(
        label='Upload GST Document',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    email_id = forms.EmailField(
        label='Email Id',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    mobile_number = forms.IntegerField(
        label='Mobile Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )

    class Meta:
        model = RecruiterModel
        fields = ['company_name', 'gst_no', 'gst_doc', 'email_id', 'mobile_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignUpFormRecruiter, self).save(commit=False)
        user.username = self.cleaned_data['email_id']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    email_id = forms.EmailField(label='Email Id',
                                widget=forms.EmailInput(attrs={'class': 'form-control'})
                                )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )

    class Meta:
        model = User
        fields = ['email_id', 'password']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'job_description', 'location', 'job_type', 'industry_category', 'salary', 'job_requirements','education_requirements', 'experience_level', 'contact_information', 'benefits', 'skills_and_qualities']

    widgets = {
        'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        'job_description': forms.Textarea(attrs={'class': 'form-control'}),
        'company_name': forms.TextInput(attrs={'class': 'form-control'}),
        'location': forms.TextInput(attrs={'class': 'form-control'}),
        'job_type': forms.Select(attrs={'class': 'form-control'}),
        'industry_category': forms.Select(attrs={'class': 'form-control'}),
        'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        'job_requirements': forms.Textarea(attrs={'class': 'form-control'}),
        'education_requirements': forms.TextInput(attrs={'class': 'form-control'}),
        'experience_level': forms.TextInput(attrs={'class': 'form-control'}),
        'contact_information': forms.TextInput(attrs={'class': 'form-control'}),
        'benefits': forms.Textarea(attrs={'class': 'form-control'}),
        'skills_and_qualities': forms.Textarea(attrs={'class': 'form-control'}),
    }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone_number', 'address', 'resume']
        widgets = {
            'job_seeker': forms.HiddenInput()
        }


class OtpLoginForm(forms.ModelForm):
    email_id = forms.EmailField(label='Email Id',
                                widget=forms.EmailInput(attrs={'class': 'form-control'})
                                )
    
    class Meta:
        model = User
        fields = ['email_id']


class OtpVerificationForm(forms.Form):
    otp = forms.IntegerField(label='Enter Your Otp', widget=forms.TextInput(attrs={'class': 'form-control'}))
