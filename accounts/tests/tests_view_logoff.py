from django.shortcuts import reverse
from boards.tests.test_views import BaseTestClass

from .. import views

class UserLogoffTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url = reverse('accounts:log-off')

    def test_redirects(self):
        # test that successful submission returns 302 status
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_correct_function(self):
        #test correct function
        response = self.client.get(self.url)
        self.assertEquals(response.resolver_match.func,views.userLogoff)