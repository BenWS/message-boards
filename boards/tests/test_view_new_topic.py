from django.shortcuts import reverse
from ..forms import CreateTopicForm
from .test_views import BaseTestClass
from .. import views

from ..models import Topic

class CreateTopicTests(BaseTestClass):

    def setUp(self):
        super().setUp()
        self.url = reverse('boards:create-topic', kwargs={'board_name':self.board.name})
        self.response = self.client.get(self.url)

    def test_redirects_if_anonymous(self):
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = reverse('accounts:login') + '?next=/boards/Hiking%2520Locations/create-topic'
        self.assertRedirects(response, expected_url)

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, CreateTopicForm)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_form_fields(self):
        self.assertContains(self.response,'type="hidden"',1)
        self.assertContains(self.response,'type="text"',1)
        self.assertContains(self.response, '<textarea',1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_returns_200_status(self):
        login_result = self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(reverse('boards:create-topic',kwargs={'board_name':self.board.name}))
        self.assertEquals(response.status_code, 200)

    def test_returns_404_status(self):
        response = self.client.get(reverse('boards:create-topic',kwargs={'board_name':self.board_name_non_existent}))
        self.assertEquals(response.status_code, 404)


    def test_correct_view(self):
        response = self.client.get(reverse('boards:create-topic', kwargs={'board_name': self.board.name}))
        self.assertEquals(response.resolver_match.func, views.createTopic)

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('boards:create-topic',kwargs={'board_name':self.board.name}))
        is_redirect_response_code = response.status_code >= 300 and response.status_code < 400
        self.assertTrue(is_redirect_response_code)

class SuccessfulCreateTopicSubmitTests(BaseTestClass):

    def setUp(self):
        super().setUp()
        self.topic_count_before = Topic.objects.all().count()
        self.url = reverse('boards:create-topic', kwargs={'board_name':self.board.name})
        self.response = self.client.post(self.url, {'subject': 'test subject','message': 'test message'})

    def test_form_submission_redirects(self):
        self.assertRedirects(self.response, reverse('boards:topics',kwargs={'board_name':self.board.name_url_formatted}))

    def test_topic_created(self):
        topic_count_after = Topic.objects.all().count()
        self.assertEquals(topic_count_after,self.topic_count_before + 1)

class InvalidCreateTopicSubmitTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.topic_count_before = Topic.objects.all().count()
        self.url = reverse('boards:create-topic', kwargs={
            'board_name': self.board.name})
        self.response = self.client.post(self.url, {
            'subject': '',
            'message': 'test message'})

    def test_redirects_form_submission_unauthorized(self):
        # test that form submission returns 'Unauthorized' HTTP status if the user *is not* logged in
        self.client.logout()
        response = self.client.post(self.url, {'subject': 'test subject', 'message': 'test message'})
        self.assertEquals(response.status_code, 302)

    def test_no_topic_created(self):
        topic_count_after = Topic.objects.all().count()
        self.assertEqual(topic_count_after,self.topic_count_before)

    def test_errors(self):
        form = self.response.context['form']
        self.assertTrue(form)

    def test_response_code(self):
        self.assertEqual(self.response.status_code,200)

