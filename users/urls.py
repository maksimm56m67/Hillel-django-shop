from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import LoginView, logout_user, registration, confirm_registration

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', registration, name='register'),
    path('confirm_registration', confirm_registration, name='confirm_registration'),
]
