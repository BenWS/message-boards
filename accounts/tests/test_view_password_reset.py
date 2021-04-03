from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views, forms as auth_forms
from django.urls import resolve
from django.core import mail

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_response_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_view(self):
        view = resolve(reverse('password_reset'))
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)

    def test_contains_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, auth_forms.PasswordResetForm)

    def test_contains_expected_fields(self):
        self.assertContains(self.response,"<input", 2)
        self.assertContains(self.response,' type="email"', 1)


class PasswordResetValidTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='NewUser', password='RedIsTheApple', email='generic_email@email.com')
        url = reverse('password_reset')
        data = {'email':'generic_email@email.com'}
        self.response = self.client.post(url, data)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 302)

    def test_assert_redirects(self):
        done_url = reverse('password_reset_done')
        self.assertRedirects(self.response, done_url)

    def test_mail_sent(self):
        self.assertEquals(len(mail.outbox), 1)

class PasswordResetNotValidTests(TestCase):

    def setUp(self):
        self.url = reverse('password_reset')
        data = {'email':''}
        self.response = self.client.post(self.url, data)

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_contains_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_nomail_sent(self):
        self.assertEquals(len(mail.outbox), 0)

class PasswordResetDoneTests(TestCase):

    def setUp(self):
        self.url = reverse('password_reset_done')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class,auth_views.PasswordResetDoneView)
