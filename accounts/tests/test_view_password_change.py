from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
import django.contrib.auth.hashers as hashers
from django.contrib.auth import views as auth_views, forms as auth_forms
from django.urls import resolve
from django.core import mail


class PasswordChangeBase(TestCase):
    def setUp(self):
        self.url = reverse('password_change')
        self.user = User.objects.create_user(username='johnny', email='email@email.com', password='123')
        self.client.login(username='johnny', password='123')

class PasswordChangeTests(PasswordChangeBase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_correct_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def test_status_code(self): # response status code of 200
        self.assertEquals(self.response.status_code, 200)

    def test_contains_form(self): # view contains correct form
        form = self.response.context['form']
        self.assertIsInstance(form, auth_forms.PasswordChangeForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_fields(self):
        self.assertContains(self.response,'<input',4)
        self.assertContains(self.response,'type="password"', 3)

class SuccessfulPasswordChangeSubmission(PasswordChangeBase):
    def setUp(self):
        super().setUp()
        data = {'old_password':'123', 'new_password1':'TheAppleIsGreen', 'new_password2':'TheAppleIsGreen'}
        self.response = self.client.post(self.url, data)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect(self):
        self.assertRedirects(self.response,reverse('password_change_done'))

    def test_password_change(self):
        self.user.refresh_from_db()
        self.assertTrue(hashers.check_password('TheAppleIsGreen', self.user.password))

class InvalidPasswordChangeSubmission(PasswordChangeBase):
    def setUp(self):
        self.url = reverse('password_change')
        self.user = User.objects.create_user(username='johnny', password='123', email='email@email.com')
        login_result = self.client.login(username='johnny', password='123')
        data = {'old_password':'123', 'new_password1':'235', 'new_password2':'234'}
        self.response = self.client.post(self.url, data)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_password_remains_same(self):
        self.user.refresh_from_db()
        self.assertTrue(hashers.check_password('123',self.user.password))