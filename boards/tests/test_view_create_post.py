from django.shortcuts import reverse

from ..models import Post
from .. import views
from .. import forms
from .test_views import BaseTestClass

class CreatePostTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('boards:create-post',
                                kwargs={
                                    'board_name': self.board.name,
                                    'topic_id': self.topic.id}))

    #TODO: Create test for invalid page visit

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

    def test_redirects_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('boards:create-post', kwargs={'board_name': self.board.name, 'topic_id': self.topic.id}))
        self.assertEquals(response.status_code, 302)

    def test_form_submission_unauthorized(self):
        #test that an unauthenticated form submission returns a status code of 401
        self.client.logout()
        response = self.client.post(
            reverse('boards:create-post', kwargs={'board_name': self.board.name, 'topic_id': self.topic.id})
                , {'subject':'Test Subject','message':'Test Message'})

        self.assertEquals(response.status_code, 302)

    def test_correct_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form,forms.CreatePostForm)

    def test_crsf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_fields(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="hidden"', 2)

class SuccessfulCreatePostSubmitTests(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url_parameters = {'board_name': self.board.name, 'topic_id': self.topic.id}
        data = {'subject': 'Test Subject',
                'message': 'Test Message',
                'post_id': self.post.id}

        self.count_posts_before = Post.objects.all().count()
        self.response = self.client.post(reverse('boards:create-post',kwargs=self.url_parameters), data)

    def test_form_submission_redirects(self):
        # test that an authenticated form submission returns a status code in the 300 range
        reverse_kwargs = {'board_name':self.board.name,'topic_id':self.topic.id}
        data = {'subject':'Test Subject','message':'Test Message','post_id':self.post.id}
        response = self.client.post(reverse('boards:create-post',kwargs=reverse_kwargs), data)

        self.assertRedirects(response, reverse('boards:view-topic', kwargs=reverse_kwargs))

    def test_post_created(self):
        count_posts_after = Post.objects.all().count()
        self.assertEquals(count_posts_after, self.count_posts_before + 1)

class InvalidCreatePostSubmitTests(BaseTestClass):
    def setUp(self):
        super().setUp()

        self.url = reverse('boards:create-post',
                           kwargs={
                               'board_name': self.board.name,
                               'topic_id': self.topic.id})

        data = {'subject': 'Test Subject',
            'message': '',
            'post_id': self.post.id}

        self.count_posts_before = Post.objects.all().count()
        self.response = self.client.post(self.url, data)

    def test_contains_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_no_post_created(self):
        count_posts_after = Post.objects.all().count()
        self.assertEquals(self.count_posts_before,count_posts_after)
