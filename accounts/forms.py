from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    # TODO: Store as reference - https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    '''
    Create validation logic, and raise custom error if any one of those validations
    is not successful 
    
    - validation that passwords match
    - validation that user does not already exist 
    - validation that email is valid  
    '''
    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        confirm_password = cleaned_data.get('confirm_password')
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if confirm_password != password:
            self.add_error('confirm_password','Password fields do not match')
            self.add_error('password', 'Password fields do not match')

        if User.objects.filter(username=username) \
                or User.objects.filter(email=email):
            raise forms.ValidationError ('User with that username or email address already exists')

        if User.objects.filter(username=username):
            self.add_error('username', 'User with that username already existssssss.')

        if User.objects.filter(email=email):
            self.add_error('email', 'User with that email address already exists.')