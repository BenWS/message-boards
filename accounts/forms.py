from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class UserSignupForm(UserCreationForm):
    email = forms.CharField(required=True, label='Email address', widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username','password']

    def clean(self):
        super().clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username,password=password)

        if user is None:
            self.add_error('username','Username/password combination does not match any record in our system')
            self.add_error('password','Username/password combination does not match any record in our system')