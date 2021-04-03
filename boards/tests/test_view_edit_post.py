from django.shortcuts import reverse

from ..models import Post
from .. import views
from .. import forms
from .test_views import BaseTestClass

class EditPostTestsBase(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.url_config_name = 'boards:edit-post'
        self.valid_url_parameters = \
            {
                'board_name': self.board.name
                , 'topic_id': self.topic.id
                , 'post_id': self.post.id
            }

        self.valid_request_response = self.client.get(
            reverse(self.url_config_name
                    , kwargs=self.valid_url_parameters))

        self.valid_submission_response = self.client.post(
            reverse(self.url_config_name + '/submit'
                    , kwargs=self.valid_url_parameters)
            , {'subject': 'Test Subject',
               'message': 'Test Message'})

class EditPostTests(EditPostTestsBase):
    def setUp(self):
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

    def test_correct_form(self):
        form = self.valid_request_response.context['form']
        self.assertIsInstance(form,forms.EditPostForm)

    def test_correct_form_fields(self):
        response = self.valid_request_response
        self.assertContains(response,'type="text"', 1)
        self.assertContains(response, '<textarea', 1)
        self.assertContains(response, '<input', 2)

    def test_csrf(self):
        self.assertContains(self.valid_request_response, 'csrfmiddlewaretoken')

    def test_not_contains_valid_feedback(self):
        self.assertNotContains(self.valid_request_response, 'valid-feedback')

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

class SuccessfulEditPostSubmissionTests(EditPostTestsBase):
    def setUp(self):
        super().setUp()
        self.data = {
            'subject': 'Edited Subject',
           'message': 'Edited Message'
        }

        self.client.post(
            reverse(self.url_config_name + '/submit',
            kwargs=self.valid_url_parameters),
            self.data
        )

    def test_updates_post(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message,self.data['message'])
        self.assertEquals(self.post.subject,self.data['subject'])

    def test_form_submission_redirects(self):
        redirect_url_parameters = {
            'board_name': self.board.name_url_formatted
            , 'topic_id': self.topic.id
        }
        response = self.valid_submission_response
        self.assertRedirects(response, reverse('boards:view-topic',kwargs=redirect_url_parameters))

class InvalidEditPostSubmissionTests(EditPostTestsBase):
    def setUp(self):
        super().setUp()
        data = {'subject':'', 'message':'Edited Message'}
        self.response = self.client.post(reverse(self.url_config_name + '/submit', kwargs=self.valid_url_parameters), data)

    def test_no_update_to_post(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message,'Test Message')

    def test_form_contains_error(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)