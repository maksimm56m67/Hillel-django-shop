import random

from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput, PasswordInput
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.conf import settings
from django.contrib import messages

from shop.helpers import send_html_mail
from .tasks import send_sms

User = get_user_model()

class Checkphone(forms.Form):
    checkphone = forms.CharField(label='checkphone', widget=forms.TextInput(attrs= {'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
        # checkphone = forms.CharField(label='checkphone', widget=forms.TextInput(attrs= {'class': 'form-control'}))
	
        class Meta:
            model = User
            fields = ['email', 'phone', 'password']

            widgets = {
                'email': TextInput(attrs= {
                    'class': 'form-control',

                }),
                'password': PasswordInput(attrs= {
                    'class': 'form-control',

                }),
                'phone': TextInput(attrs= {
                    'class': 'form-control',

                }),   
            }
            
 
             
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.is_active = False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        context = {
            'email': user.email,
            'domain': settings.DOMAIN,
            'site_name': 'SHOP',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'subject': 'Confirm registration'
        }
        subject_template_name = 'emails/registration/registration_confirm_subject.txt'  # noqa
        email_template_name = 'emails/registration/registration_confirm_email.html'  # noqa
        send_html_mail(
            subject_template_name,
            email_template_name,
            from_email=settings.SERVER_EMAIL,
            to_email=user.email,
            context=context
        )

        if self.cleaned_data.get('phone'):
            code = random.randint(10000, 99999)
            cache.set(f'{str(user.id)}_code', code, timeout=60)
            send_sms.delay(self.cleaned_data.get('phone'), code)
        return user  

  
