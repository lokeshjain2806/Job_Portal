from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.views import View
from .forms import SignUpFormRecruiter, SignUpFormSeeker, LoginForm


# Create your views here.
def Home(request):
    return render(request, 'base.html')


class SignUpSeekerView(View):
    def get(self, request):
        form = SignUpFormSeeker
        return render(request, 'signupseeker.html', {'form': form})


class SignUpRecruiterView(View):
    def get(self, request):
        form = SignUpFormRecruiter
        return render(request, 'signuprecruiter.html', {'form': form})


class Login(View):
    def get(self, request):
        form = LoginForm
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