from django.shortcuts import reverse
from django.urls import resolve
from django.contrib.auth import views as auth_views

from boards.tests.test_views import BaseTestClass
from .. import views

class UserLoginTests(BaseTestClass):

    def setUp(self):
        super().setUp()
        self.non_existent_username = 'Non-existent User'
        self.non_existent_password = 'Non-existent Password'
        self.url = reverse('accounts:login')

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code,200)

    def test_successful_form_redirects(self):
        # test that submission for existing user redirects
        response = self.client.post(self.url
                                    , {'username': self.test_username
                                        , 'password': self.test_password})
        self.assertEquals(response.status_code, 302)

    def test_unsuccessful_form_displays_error(self):
        # test that unsuccessful form submission refreshes the page with 'invalid login' message
        response = self.client.post(self.url
                                    , {'username': self.non_existent_username
                                        , 'password': self.non_existent_password})

        self.assertTrue(response.context['form'].errors)

    def test_correct_view(self):
        # test that URL resolves to intended view function
        response = self.client.get(self.url)
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, auth_views.LoginView)