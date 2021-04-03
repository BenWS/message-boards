from django.test import TestCase
from .. import forms

class SignUpFormTests(TestCase):

    def test_field_sequence(self):
        form = forms.UserSignupForm()
        actual = list(form.fields)
        expected = ['username','email','password1','password2']
        self.assertSequenceEqual(actual,expected)