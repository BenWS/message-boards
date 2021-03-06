from django.urls import path
from accounts import views as account_views

app_name = 'accounts'

urlpatterns = [
    path('sign-up', account_views.userSignup, name='sign-up')
]