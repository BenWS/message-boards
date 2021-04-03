from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    ##/
    path('',views.BoardListView.as_view(),name='index'),
    path('<str:board_name>/topics',views.TopicListView.as_view(), name='topics'),
    # path('<str:board_name>/topics',views.topics,name='topics'),
    path('<str:board_name>/topic/<int:topic_id>',views.PostListView.as_view(),name='view-topic'),
    path('<str:board_name>/create-topic',views.createTopic,name='create-topic'),
    path('<str:board_name>/create-topic/submit',views.createTopic,name='create-topic/submit'),
    path('<str:board_name>/topic/<int:topic_id>/create-post',views.createPost,name='create-post'),
    path('<str:board_name>/topic/<int:topic_id>/create-post/submit',views.createPost,name='create-post/submit'),
    path('<str:board_name>/topic/<int:topic_id>/edit-post/<int:post_id>',views.editPost,name='edit-post'),
    path('<str:board_name>/topic/<int:topic_id>/edit-post/<int:post_id>/submit',views.editPost, name='edit-post/submit'),
    path('contact-admin',views.contactAdmin,name='contact-admin')
]

def printUrlPatterns():
    for url in urlpatterns:
        print(str(url.callback.__name__).strip() + ","
              + '/' + str(url.pattern).strip() + ","
              + url.name)