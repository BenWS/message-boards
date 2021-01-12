from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from boards.models import Board, Topic, Post
from boards import views


class BaseTestClass(TestCase):
    def setUp(self):
        self.test_password = 'Test Password'
        self.test_username = 'Test User'
        self.test_email = 'testemail@test.com'
        self.client = Client()
        self.board = Board.objects.create(name="Hiking Locations", description="This is a description of the board")
        self.board_alternate = Board.objects.create(name="Alternate Test Board", description="This is a description of the board")
        self.user = User.objects.create_user(username=self.test_username, password=self.test_password, email=self.test_email)
        self.client.login(username=self.test_username, password=self.test_password)
        self.user_alternate = User.objects.create_user(username='Alternate User', password=self.test_password)
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

# Create your tests here.
class HomeTests(BaseTestClass):

    def test_returns_200_status(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.status_code,200)

    def test_correct_view(self):
        client = Client()
        response = client.get(reverse('boards:index'))
        self.assertEquals(response.resolver_match.func, views.home)

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
        client = Client()
        response = client.get(reverse("boards:topics", args=["Hiking Locations"]))
        self.assertEquals(response.resolver_match.func,views.topics)

class ViewTopicTests(BaseTestClass):

    def test_returns_200_status(self):
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        self.assertEquals(response.status_code,200)


    def test_returns_404_status(self):
        board_name_non_existent = "Board Name"
        topic_id_non_existent = max(topic.id for topic in Topic.objects.all()) + 1

        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": topic_id_non_existent}))
        self.assertEquals(response.status_code, 404)

    def test_correct_view(self):
        response = self.client.get(reverse("boards:view-topic", kwargs={"board_name": self.board.name, "topic_id": self.topic.id}))
        self.assertEquals(response.resolver_match.func,views.viewTopic)

class CreateTopicTests(BaseTestClass):

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

class CreatePostTests(BaseTestClass):

    def test_correct_view(self):
        # test that URL resolves to intended view
        response = self.client.get(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id}))
        self.assertEquals(response.resolver_match.func, views.createPost)

    def test_returns_200_status(self):
        #test that URL returns a 200 HTTP status code for an existing topic
        response = self.client.get(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id}))
        self.assertEquals(response.status_code, 200)

    def test_returns_406_status(self):
        self.client.login(username=self.test_username,password=self.test_password)

        #client submits a post request for creating a new post,
        # and attempt for replying to post not in topic should return 'Non Allowed' response

        response = self.client.post(reverse('boards:create-post/submit'
                                , kwargs={'board_name': self.board.name, 'topic_id': self.topic.id})
                                    , {'subject':'Test Subject','message':'Test Message', 'post_id': self.post_topic_alternate.id})

        self.assertEquals(response.status_code, 406)

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
        self.client.login(username=self.test_username,password=self.test_password)
        response = self.client.post(reverse('boards:create-post',kwargs={'board_name':self.board.name,'topic_id':self.topic.id})
                                   , {'subject':'Test Subject','message':'Test Message','post_id':self.post.id})

        self.assertEquals(response.status_code, 302)

    def test_form_submission_unauthorized(self):
        #test that an unauthenticated form submission returns a status code of 401
        self.client.logout()
        response = self.client.post(
            reverse('boards:create-post', kwargs={'board_name': self.board.name, 'topic_id': self.topic.id})
                , {'subject':'Test Subject','message':'Test Message'})

        self.assertEquals(response.status_code, 401)

class TestEditPost(BaseTestClass):

    def setUp(self):
        self.url_config_name = 'boards:edit-post'
        super().setUp()

    def test_correct_view(self):
        # test that the URL matches the correct view
        response = self.client.get(
            reverse(self.url_config_name
                    , kwargs={'board_name': self.board.name, 'topic_id': self.topic.id, 'post_id':self.post.id}))
        self.assertEquals(response.resolver_match.func, views.editPost)

    def test_edit_page_200_status(self):
        response = self.client.get(reverse(self.url_config_name
                                           , kwargs={'board_name': self.board.name
                                           , 'topic_id': self.topic.id
                                           , 'post_id': self.post.id}))

        self.assertEquals(response.status_code, 200)

    def test_form_submission_redirects(self):
        response = self.client.post(reverse(self.url_config_name + '/submit'
                                            , kwargs={'board_name': self.board.name
                                            , 'topic_id': self.topic.id
                                            , 'post_id': self.post.id})
                                    , {'subject':'Test Subject', 'message':'Test Message'})

        self.assertEquals(response.status_code, 302)

    def test_get_post_unrelated_board_topic(self):
        response_unrelated_topic = self.client.get(reverse(self.url_config_name
                                           , kwargs={'board_name': self.board.name
                                                     , 'topic_id': self.topic_alternate.id
                                                     , 'post_id': self.post.id}))

        response_unrelated_board = self.client.get(reverse(self.url_config_name
                                           , kwargs={'board_name': self.board_alternate.name
                                                     , 'topic_id': self.topic.id
                                                     , 'post_id': self.post.id}))

        view_returns_400_status = \
            response_unrelated_board.status_code == 400 \
            and response_unrelated_topic.status_code == 400

        self.assertTrue(view_returns_400_status)

    # test that successful form submission returns redirect status code

    def test_get_non_existent_board_topic(self):
        # test that user trying to access a non-existent board, topic, or post receives a 404
        response_non_existent_board = self.client.get(reverse(self.url_config_name
                                , kwargs={'board_name':self.board_name_non_existent
                                          , 'topic_id':self.topic.id
                                          , 'post_id':self.post.id}))

        response_non_existent_topic = self.client.get(reverse(self.url_config_name
                              , kwargs={'board_name': self.board.name
                                        , 'topic_id': self.topic_id_non_existent
                                        , 'post_id': self.post.id}))

        response_non_existent_post = self.client.get(reverse(self.url_config_name
                            , kwargs={'board_name': self.board.name
                                    , 'topic_id': self.topic.id
                                    , 'post_id': self.post_id_non_existent}))

        if response_non_existent_post.status_code == 404 \
                and response_non_existent_topic.status_code == 404 \
                and response_non_existent_board.status_code == 404:

            non_existent_returns_404 = True

        self.assertTrue(non_existent_returns_404)

    def test_get_edit_page_another_users_post(self):
        # test that the user cannot access screen via GET request for editing another user's post - only their own
        response = self.client.get(reverse(self.url_config_name
                                , kwargs = {'board_name':self.board.name
                                            , 'topic_id': self.topic.id
                                            , 'post_id':self.post_user_alternate.id}))

        self.assertEquals(response.status_code, 403)

    def test_submit_edit_another_users_post(self):
        # test that the user cannot submit a POST request to edit another user's post
        response = self.client.post(reverse(self.url_config_name + '/submit'
                                            , kwargs={'board_name': self.board.name
                                            , 'topic_id': self.topic.id
                                            , 'post_id': self.post_user_alternate.id})
                                    , {'subject':'Test Subject', 'message':'Test Message'})

        self.assertEquals(response.status_code, 403)

    def test_anonymous_user_redirected(self):
        self.client.logout()
        # test that an anonymous user is redirected to the user sign-in page
        response_get_request = self.client.get(reverse(self.url_config_name
                                                    , kwargs={'board_name': self.board.name
                                                    , 'topic_id': self.topic.id
                                                    , 'post_id': self.post.id}))

        response_post_request = self.client.post(reverse(self.url_config_name + '/submit'
                                                    , kwargs={'board_name': self.board.name
                                                    , 'topic_id': self.topic.id
                                                    , 'post_id': self.post.id})
                                                 , {'message':'Test Message', 'subject':'Test Subject'})

        response_valid = \
            response_get_request.status_code == 302 \
            and response_post_request.status_code == 302

        self.assertTrue(response_valid)

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

class UserSignUpTests(BaseTestClass):

    def setUp(self):
        self.url_config_name = 'boards:sign-up'
        self.url = reverse(self.url_config_name)
        super().setUp()

    def test_successful_submission_returns_302(self):
        # test that successful submission returns 302 status
        response = self.client.post(self.url
                         , {'username': self.user.username
                            , 'email': self.user.email
                            , 'password': self.user.password
                            , 'confirm_password': self.user.password})

        self.assertEquals(response.status_code, 302)

    def test_successful_submission_redirects_home_page(self):
        # test that successful submission redirects user to Home Page
        response = self.client.post(self.url
                                    , {'username': self.user.username
                                        , 'email': self.user.email
                                        , 'password': self.user.password
                                        , 'confirm_password': self.user.password})

        print("Hello world!")


    # test that successful submission logs the user in
    # test that unsuccessful submission redirects the user to the same page
    # test that URL resolves to intended view function
    pass


class UserLoginTests(BaseTestClass):
    # test that successful form redirects user
    # test that unsuccessful form submission refreshes the page with 'invalid login' message
    # test that URL resolves to intended view function
    pass

class UserLogoffTests(BaseTestClass):
    # test that successful submission returns 302 status
    # test that successful submission returns user with anonymous verbiage
    pass