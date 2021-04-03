from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse

from accounts import views as account_views

app_name = 'accounts'

urlpatterns = [
    path('sign-up', account_views.userSignup, name='sign-up'),
    path('log-off', account_views.userLogoff, name='log-off'),
    path('log-in', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('my-account', account_views.UserUpdateView.as_view(), name='my-account')
]