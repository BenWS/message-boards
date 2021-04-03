from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth import views as auth_views, forms as auth_forms
from django.urls import resolve
from django.core import mail

class PasswordResetMailTests(TestCase):
    def setUp(self):
        self.url = reverse('password_reset')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.response = self.client.post(self.url,{'email':self.user.email})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(self.email.subject,'[Django Boards] Please reset your password')

    def test_email_body(self):
        context = self.response.context
        uid = context.get('uid')
        token = context.get('token')
        url = reverse('password_reset_confirm',
                      kwargs = {
                          'uidb64': uid,
                          'token': token
                      })

        self.assertIn(url, self.email.body)
        self.assertIn(self.user.username, self.email.body)
        self.assertIn(self.user.email, self.email.body)


    def test_email_recipient(self):
        self.assertEquals(self.email.to[0],self.user.email)
