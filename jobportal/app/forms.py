from django import forms


class SignUpFormSeeker(forms.Form):
    name = forms.CharField(label='Full Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
    email_id = forms.EmailField(label='Email Id',
                           widget=forms.EmailInput(attrs={'class': 'form-control'})
                           )
    mobile_number = forms.IntegerField(label='Mobile Number',
                                       widget=forms.TextInput(attrs={'class': 'form-control'})
                                       )
    work_experience = forms.ChoiceField(
        label='Work Experience',
        choices=(
            ('Fresher', 'Fresher'),
            ('Experienced', 'Experienced'),
        ),
        widget=forms.Select(attrs={'class': 'form-control work-experience-label'}),
    )
    resume = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                       )
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                       )


class SignUpFormRecruiter(forms.Form):
    company_name = forms.CharField(label='Company Full Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
    gst_no = forms.CharField(label='GSTIN Number', widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
    gst_doc = forms.FileField(label='Upload GST Document', widget=forms.FileInput(attrs={'class': 'form-control'}))
    email_id = forms.EmailField(label='Email Id',
                           widget=forms.EmailInput(attrs={'class': 'form-control'})
                           )
    mobile_number = forms.IntegerField(label='Mobile Number',
                                       widget=forms.TextInput(attrs={'class': 'form-control'})
                                       )
    password = forms.CharField(label='Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                       )
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                       )


class LoginForm(forms.Form):
    email_id = forms.EmailField(label='Email Id',
                                widget=forms.EmailInput(attrs={'class': 'form-control'})
                                )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )