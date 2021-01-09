from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from boards.models import Board, Topic
from boards import views

# Create your tests here.
class HomeTests(TestCase):

    def test_returns_200_status(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.status_code,200)

    def test_correct_view(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.resolver_match.func, views.home)

class TopicTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name="Hiking Locations", description="This is a description of the board")

    def test_returns_200_status(self):
        client = Client()
        response = client.get(reverse("boards:topics", args=["Hiking Locations"]))
        self.assertEquals(response.status_code,200)

    def test_returns_404_status(self):
        client = Client()
        response = client.get(reverse("boards:topics", args=["Non-existent Board"]))
        self.assertEquals(response.status_code, 404)

    def test_correct_view(self):
        client = Client()
        response = client.get(reverse("boards:topics", args=["Hiking Locations"]))
        self.assertEquals(response.resolver_match.func,views.topics)

class ViewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Hiking Locations", description="This is a description of the board")
        self.user = User.objects.create(username="TestUser")
        self.topic = Topic.objects.create(
            subject="Where are some good places to hike?",
            board=self.board,
            created_by=self.user,
            updated_by=self.user
        )

        self.client = Client()

    def test_returns_200_status(self):
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        self.assertEquals(response.status_code,200)


    def test_returns_404_status(self):
        board_name_non_existent = "Board Name"
        topic_id_non_existent = self.topic.id + 1

        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": topic_id_non_existent}))
        self.assertEquals(response.status_code, 404)

    def test_correct_view(self):
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        self.assertEquals(response.resolver_match.func,views.viewTopic)

class CreateTopicTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser",password="TestPassword")
        self.board = Board.objects.create(name="Hiking Locations", description="This is a description of the board")

    def test_returns_200_status(self):
        login_result = self.client.login(username="TestUser", password="TestPassword")
        response = self.client.get(reverse('boards:create-topic',kwargs={'board_name':self.board.name}))
        self.assertEquals(response.status_code, 200)

    def test_form_submission_redirects_if_logged_in(self):
        # test that form submission redirects if user is logged in
        login_result = self.client.login(username="TestUser", password="TestPassword")
        response = self.client.post(reverse('boards:create-topic', kwargs={'board_name':self.board.name}),{'subject':'test subject', 'message':'test message'})
        is_redirect_response_code = response.status_code >= 300 and response.status_code < 400
        self.assertTrue(is_redirect_response_code)

    def test_form_submission_unauthorized(self):
        # test that form submission returns 'Unauthorized' HTTP status if the user *is not* logged in
        response = self.client.post(reverse('boards:create-topic', kwargs={'board_name': self.board.name}), {'subject': 'test subject', 'message': 'test message'})
        self.assertEquals(response.status_code, 401)

    def test_correct_view(self):
        response = self.client.get(reverse('boards:create-topic', kwargs={'board_name': self.board.name}))
        self.assertEquals(response.resolver_match.func, views.createTopic)

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('boards:create-topic',kwargs={'board_name':self.board.name}))
        is_redirect_response_code = response.status_code >= 300 and response.status_code < 400
        self.assertTrue(is_redirect_response_code)

class CreatePostTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.board = Board.objects.create(name='TestName', description='TestDescription')
        self.user = User.objects.create_user(username='TestUser', password='TestPassword')
        self.topic = Topic.objects.create(subject='TestSubject',created_by=self.user, updated_by=self.user, board=self.board)

    def test_correct_view(self):
        # test that URL resolves to intended view
        response = self.client.get(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id}))
        self.assertEquals(response.resolver_match.func, views.createPost)

    def test_returns_200_status(self):
        #test that URL returns a 200 HTTP status code for an existing topic
        response = self.client.get(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id}))
        self.assertEquals(response.status_code, 200)

    def test_returns_400_status(self):
        # test that URL returns a 404 HTTP status code for a non-existent topic
        #  OR non-existent board
        non_existent_topic = self.topic.id + 1
        non_existent_board = self.board.name + 'additionalText'
        response_non_existent_topic = \
            self.client.get(reverse('boards:create-post'
                                    , kwargs={'board_name': self.board.name, 'topic_id': non_existent_topic}))

        response_non_existent_board = \
            self.client.get(reverse('boards:create-post'
                                    , kwargs={'board_name': non_existent_board, 'topic_id': self.topic.id}))

        if (
            response_non_existent_board.status_code == 404
            or response_non_existent_topic.status_code == 404
        ):
            submission_returns_404 = True
        else:
            submission_returns_404 = False

        self.assertTrue(submission_returns_404)

    def test_form_submission_redirects(self):
        # test that an authenticated form submission returns a status code in the 300 range
        self.client.login(username='TestUser',password='TestPassword')
        response = self.client.post(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id})
                                   , {'subject':'Test Subject','message':'Test Message'})

        self.assertEquals(response.status_code, 302)

    def test_form_submission_unauthorized(self):
        #test that an unauthenticated form submission returns a status code of 401
        response = self.client.post(
            reverse('boards:create-post', kwargs={'board_name': self.board.name, 'topic_id': self.topic.id})
                , {'subject':'Test Subject','message':'Test Message'})

        self.assertEquals(response.status_code, 401)
