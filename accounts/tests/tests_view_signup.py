from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import forms as auth_forms
from boards.tests.test_views import BaseTestClass
from django.contrib.auth.models import User

from .. import forms
from .. import views as view_accounts

class SignUpViewTests(BaseTestClass):

    # test that visiting form returns successful (200) status code
    def setUp(self):
        self.url_config_name = 'accounts:sign-up'
        self.url = reverse(self.url_config_name)
        super().setUp()

    def test_correct_view(self):
        # test that URL resolves to intended view function
        response = self.client.get(self.url)
        self.assertEquals(response.resolver_match.func, view_accounts.userSignup)

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code,200)

    def test_contains_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], forms.UserSignupForm)

    def test_contains_crsf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response,'csrfmiddlewaretoken')

    def test_contains_fields(self):
        response = self.client.get(self.url)
        self.assertContains(response,'<input', 5)
        self.assertContains(response,'type="password"',2)
        self.assertContains(response,'type="text"', 1)
        self.assertContains(response,'type="email"', 1)


class SignUpSuccessfulSubmissionTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url_config_name = 'accounts:sign-up'
        self.url = reverse(self.url_config_name)
        self.new_username = 'NewUser'
        self.new_password = 'BananaGrapevine99'
        self.new_email = 'newemail@email.com'

        data = {
            'username': self.new_username
            , 'email':self.new_email
            , 'password1': self.new_password
            , 'password2': self.new_password
        }

        self.response = self.client.post(self.url, data)


    def test_successful_submission_returns_302(self):
        # test that successful submission returns 302 status
        self.assertEquals(self.response.status_code, 302)

    def test_successful_submission_redirects_home_page(self):
        # test that successful submission redirects user to Home Page
        self.assertEquals(self.response.status_code, 302)

class SignUpInvalidSubmissionTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url_config_name = 'accounts:sign-up'
        self.url = reverse(self.url_config_name)

    def test_existing_user_returns_error(self):
        # test that sign-up submission for existing user returns an error
        data = {
            'username': self.test_username
            , 'password1': self.test_password
            , 'password2': self.test_password
        }

        response = self.client.post(self.url, data)
        self.assertTrue(response.context['form'].errors)

    def test_returns_200_status(self):
        data = {
            'username': self.test_username
            , 'password1': self.test_password
            , 'password2': self.test_password
        }

        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code,200)

    def test_empty_form_fields(self):
        data = {
             'username':''
            , 'password1':''
            , 'password2':''
        }

        response = self.client.post(self.url,data)
        self.assertTrue(response.context['form'].errors)

    def test_mismatching_passwords(self):
        data = {
            'username': 'NewUser'
            , 'password1': 'BananaGrapevine98'
            , 'password2': 'BananaGrapevine99'
        }

        response = self.client.post(self.url, data)
        self.assertTrue(response.context['form'].errors)

    def test_user_not_created(self):
        self.client.post(self.url, {'NewUser': ''})
        self.assertFalse(User.objects.filter(username='NewUser'))