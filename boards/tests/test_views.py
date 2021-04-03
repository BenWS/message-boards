from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.urls import resolve

from ..models import Board, Topic, Post
from .. import views
from .. import forms


class BaseTestClass(TestCase):
    def setUp(self):
        self.test_password = 'TestPassword'
        self.test_username = 'TestUser'
        self.test_email = 'testemail@test.com'
        self.client = Client()
        self.board = Board.objects.create(name="Hiking Locations", description="This is a description of the board")
        self.board_alternate = Board.objects.create(name="Alternate Test Board", description="This is a description of the board")
        self.user = User.objects.create_user(username=self.test_username, password=self.test_password, email=self.test_email)
        self.user_alternate = User.objects.create_user(username='Alternate User', password=self.test_password)
        login_result = self.client.login(username=self.test_username, password=self.test_password)
        self.topic = Topic.objects.create(
            subject="Where are some good places to hike?",
            board=self.board,
            created_by=self.user,
            updated_by=self.user
        )

        self.topic_alternate = Topic.objects.create(subject='TestSubject2'
                                                    , created_by=self.user
                                                    , updated_by=self.user
                                                    , board=self.board)
        self.post = Post.objects.create(
            subject='Test Subject'
            , message='Test Message'
            , topic=self.topic
            , created_by=self.user
            , updated_by=self.user)

        self.post_topic_alternate = Post.objects.create(
            subject='Test Subject'
            , topic=self.topic_alternate
            , message='Test Message'
            , created_by=self.user_alternate
            , updated_by=self.user_alternate)

        self.post_user_alternate = Post.objects.create(
            subject='Test Subject'
            , topic=self.topic
            , message='Test Message'
            , created_by=self.user_alternate
            , updated_by=self.user_alternate)

        self.topic_id_non_existent = max(topic.id for topic in Topic.objects.all()) + 1
        self.board_name_non_existent = 'Non-existent Board'
        self.post_id_non_existent = max(post.id for post in Post.objects.all()) + 1

class HomeTests(BaseTestClass):

    def test_returns_200_status(self):
        response = self.client.get(reverse('boards:index'))
        self.assertEquals(response.status_code,200)

    def test_correct_view(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        view = resolve(reverse('boards:index'))
        self.assertEquals(view.func.view_class, views.BoardListView)

class TopicTests(BaseTestClass):
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
        view = resolve(reverse('boards:topics', args=["Hiking Locations"]))
        self.assertEquals(view.func.view_class,views.TopicListView)

class ViewTopicTests(BaseTestClass):

    def test_returns_200_status(self):
        url = reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)


    def test_returns_404_status(self):
        board_name_non_existent = "Board Name"
        topic_id_non_existent = max(topic.id for topic in Topic.objects.all()) + 1

        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": topic_id_non_existent}))
        self.assertEquals(response.status_code, 404)

    def test_correct_view(self):
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        view = resolve(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        self.assertEquals(view.func.view_class,views.PostListView)

class ContactAdminTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url_config_name = 'boards:contact-admin'

    # test that URL resolves to correct view
    def test_returns_correct_view(self):
        response = self.client.get(reverse(self.url_config_name))
        self.assertEquals(response.resolver_match.func, views.contactAdmin)

    # test that page returns 200 status
    def test_returns_200_status(self):
        response = self.client.get(reverse(self.url_config_name))
        self.assertEquals(response.status_code, 200)

