from django.urls import path, include
from django.contrib import admin
from accounts import views as account_views

app_name = 'myproject'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('boards/', include('boards.urls'))
]
