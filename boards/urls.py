from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    ##/
    path('',views.home,name='index'),
    ##/boards/hiking-locations/topics
    path('<str:board_name>/topics',views.topics,name='topics'),
    ##/boards/hiking-locations/topic/2
    path('<str:board_name>/topic/<int:topic_id>',views.viewTopic,name='view-topic'),
    ##/boards/hiking-locations/create-topic
    path('<str:board_name>/create-topic',views.createTopic,name='create-topic'),
    ##/boards/hiking-locations/create-topic/submit
    path('<str:board_name>/create-topic/submit',views.createTopic,name='create-topic/submit'),
    ##/boards/hiking-locations/topic/3/create-post?post_id=2
    path('<str:board_name>/topic/<int:topic_id>/create-post',views.createPost,name='create-post'),
    path('<str:board_name>/topic/<int:topic_id>/create-post/submit',views.createPost,name='create-post/submit'),
    ##/boards/hiking-locations/topic/2/edit-post/1
    path('<str:board_name>/topic/<int:topic_id>/edit-post/<int:post_id>',views.editPost,name='edit-post'),
    path('<str:board_name>/topic/<int:topic_id>/edit-post/<int:post_id>/submit',views.editPost,name='edit-post/submit'),
    #/contact-admin
    path('contact-admin',views.contactAdmin,name='contact-admin'),
    path('sign-up', views.userSignup, name='sign-up'),
    path('log-in', views.userLogin, name='login'),
    path('log-off', views.userLogoff, name='log-off')
]

def printUrlPatterns():
    for url in urlpatterns:
        print(str(url.callback.__name__).strip() + ","
              + '/' + str(url.pattern).strip() + ","
              + url.name)