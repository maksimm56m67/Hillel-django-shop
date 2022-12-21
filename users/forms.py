from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from users.model_forms import RegisterForm
from django.shortcuts import render, redirect
from users.models import User
from django.contrib.auth.hashers import make_password

class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}), required=False)
    phone = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')

        if not username and not phone:
            messages.error(self.request, 'Email or phone number is required.')
            raise ValidationError('Email or phone number is required.')

        if password:
            kwargs = {'password': password, 'username': username}
            if phone and not username:
                kwargs.pop('username')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
    
