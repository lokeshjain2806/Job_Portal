from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import JobSeekerModel, RecruiterModel, Job, JobApplication, MyUser, ContactModel, Location
from django.contrib.auth.forms import SetPasswordForm


class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''


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
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
    category = forms.ChoiceField(
        label='Category',
        choices=JobSeekerModel.INDUSTRY_CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = JobSeekerModel
        fields = ['profile_image', 'name', 'email', 'mobile_number', 'work_experience', 'resume', 'category']


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
    company_image = forms.ImageField(label='Company Logo', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)

    class Meta:
        model = RecruiterModel
        fields = ['company_image', 'company_name', 'gst_no', 'gst_doc', 'email_id', 'mobile_number']

    def save(self, commit=True):
        user = super(SignUpFormRecruiter, self).save(commit=False)
        user.username = self.cleaned_data['email_id']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                                )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )

    class Meta:
        model = MyUser
        fields = ['username', 'password']


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
        'company_image': forms.FileInput(attrs={'class': 'form-control'}),
    }


class ReadOnlyEmailInput(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['readonly'] = 'readonly'
        return super().render(name, value, attrs, renderer)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone_number', 'address', 'resume']
        widgets = {
            'job_seeker': forms.HiddenInput(),
            'email': ReadOnlyEmailInput(),
        }


class OtpLoginForm(forms.ModelForm):
    email_id = forms.EmailField(label='Email Id',
                                widget=forms.EmailInput(attrs={'class': 'form-control'})
                                )

    class Meta:
        model = MyUser
        fields = ['email_id']


class OtpVerificationForm(forms.Form):
    otp = forms.IntegerField(label='Enter Your Otp', widget=forms.TextInput(attrs={'class': 'form-control'}))


class RegistrationForm(UserCreationForm):
    type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=MyUser.REGISTRATION_CHOICES,
    )

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['message', 'name', 'email', 'subject']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LocationForm(forms.ModelForm):
    location_name = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name='location_name',
        empty_label="Select a Location"
    )

    class Meta:
        model = Location
        fields = ['location_name']