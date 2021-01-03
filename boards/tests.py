from django.test import TestCase, Client
from django.shortcuts import reverse
from boards.models import Board, Topic
from django.contrib.auth.models import User
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
        topic_id_non_existent = 3

        # make web request
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": board_name_non_existent, "topic_id": self.topic.id}))
        # check if web request response code is 404
        self.assertEquals(response.status_code, 404)

    def test_correct_view(self):
        pass