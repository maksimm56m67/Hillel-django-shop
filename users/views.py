import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import CustomAuthenticationForm
from users.model_forms import RegisterForm, Checkphone

from django.shortcuts import render, redirect
from users.models import User
from django.urls import is_valid_path
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as user_login
from django.contrib.auth.hashers import make_password
from django.views.generic import FormView, RedirectView

from django.core.cache import cache
from users.forms import CustomAuthenticationForm
from users.model_forms import RegistrationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str as force_text 
from django.contrib.auth import get_user_model


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back {form.get_user().email}!')
        return super().form_valid(form)


def logout_user(request):
    logout(request)
    return redirect('login')


def registration(request):
    context = {
        'confirm_form': Checkphone(),
        'form': RegisterForm(),
        'error': None,
        'title': 'registration',
    }
    if request.method == 'GET':
        return render(request, 'registration/registration.html', context)  # Вывести форму на страницу
        
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        check_form = Checkphone(request.POST)
        has_user = User.objects.filter(email=form.data['email']).exists()

        if has_user:
            messages.error(request, 'this email already exists. Maybe you already have an account?')
            context['error'] = 'this email already exists. Maybe you already have an account?'
            return render(request, 'registration/registration.html', context)
        if len(form.data['password']) < 6:
            messages.error(request, 'Password must be at least 6 characters long')
            context['error'] = 'Password must be at least 6 characters long'
            return render(request, 'registration/registration.html', context)

        password = make_password(form.data['password'])

        user = User.objects.create(
            email=form.data['email'],
            phone=form.data['phone'],
            password=password,
            is_active=False
        )  
        code = random.randint(10000, 99999)
        
        messages.success(request, f'User created successfully')
        context['error'] = f'User created successfully'
        
        messages.error(request, f'To confirm the user write the numbers that came to your phone. {code}')
        context['error'] = f'To confirm the user write the numbers that came to your phone. {code}'
        return render(request, 'registration/confirm_registration.html', context)      

                
    
def confirm_registration(request):
    context = {
        'confirm_form': Checkphone(),
        'form': RegisterForm(),
        'error': None,
        'title': 'confirm_registration',
    }
    if request.method == 'GET':
        return render(request, 'registration/confirm_registration.html', context)  # Вывести форму на страницу
        
    elif request.method == 'POST':
        User = get_user_model() 
        form = RegisterForm(request.POST)
        check_form = Checkphone(request.POST)


        code = random.randint(10000, 99999)
        if code != check_form.data['checkphone']:
            messages.success(request, f'Phone was confirmed')
            context['error'] = f'Phone was confirmed'
            # user.is_active = True
            # user.save()
            return render(request, 'registration/registration.html', context)  
        else:       
            messages.error(request, f'To confirm the user write the numbers that came to your phone. {code}')
            context['error'] = f'To confirm the user write the numbers that came to your phone. {code}'
            return render(request, 'registration/confirm_registration.html', context)      
          