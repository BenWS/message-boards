from django.urls import path, include
from django.contrib import admin
import django.contrib.auth.views as auth_views

from accounts import views as account_views

app_name = 'myproject'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('boards/', include('boards.urls')),
    path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z_\-]{1,13}-[0-9A-Za-z_\-]{1,20})',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('settings/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done')
]
