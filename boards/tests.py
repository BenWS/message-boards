from django.test import TestCase, Client
from django.shortcuts import reverse
from boards.models import Board
from boards import views

# Create your tests here.
class HomeTests (TestCase):

    def test_returns_200_status(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.status_code,200)

    def test_correct_view(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.resolver_match.func, views.home)