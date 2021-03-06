from django.test import TestCase
from django.shortcuts import reverse


from boards.tests import BaseTestClass
from accounts import views as view_accounts

class UserSignUpTests(BaseTestClass):

    def setUp(self):
        self.url_config_name = 'accounts:sign-up'
        self.url = reverse(self.url_config_name)
        self.new_username = 'ThisIsNotATest'
        self.new_password = 'NewWayOfDoingThing1999'
        self.new_email = 'newemail@email.com'
        super().setUp()

    def test_successful_submission_returns_302(self):
        # test that successful submission returns 302 status
        response = self.client.post(self.url
                         , {'username': self.new_username
                            , 'password1': self.new_password
                            , 'password2': self.new_password})

        self.assertEquals(response.status_code, 302)

    def test_successful_submission_redirects_home_page(self):
        # test that successful submission redirects user to Home Page
        response = self.client.post(self.url
                                    , {'username': self.new_username
                                        , 'password1': self.new_password
                                        , 'password2': self.new_password})

        self.assertEquals(response.status_code, 302)

    def test_submission_existing_user_returns_error(self):

        # test that sign-up submission for existing page returns an error
        response = self.client.post(self.url
                                    , {'username': self.user.username
                                        , 'password1': self.user.password
                                        , 'password2': self.user.password})

        error_string = 'A user with that username already exists.'
        string_found = error_string in str(response.content)

        self.assertTrue(string_found)

    def test_correct_view(self):
        # test that URL resolves to intended view function
        response = self.client.get(self.url)
        self.assertEquals(response.resolver_match.func, view_accounts.userSignup)


    def test_submission_redirects(self):
        # test that successful submission redirects user to Home Page
        response = self.client.post(self.url
                                    , {'username': self.new_username
                                        , 'password1': self.new_password
                                        , 'password2': self.new_password})

        self.assertEquals(response.status_code,302)