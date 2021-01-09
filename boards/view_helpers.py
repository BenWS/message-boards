from boards.models import *
from django.db.models import Max

temporary_user_id = 1

def getQueryDictItem(request, key):
    #NOTE: I should include handling for POST and other methods as well
    try:
        value = request.GET[key]
    except KeyError:
        value = None
        return value


def getTopicsByBoard(board_id):
    topics = Topic.objects.filter(board_id=board_id)

    topics = [
        {
            'id':topic.id,
            'subject':topic.subject,
            'created_by': topic.created_by.username,
            'count_posts': Post.objects.filter(topic=topic).count(),
            'last_post_user': '' if len(Post.objects.filter(topic=topic))==0 else Post.objects.filter(topic=topic).order_by('-updated_by')[0].created_by.username,
            'last_post_time': '' if len(Post.objects.filter(topic=topic))==0 else Post.objects.filter(topic=topic).order_by('-updated_by')[0].created_at
        }
        for topic
        in topics
    ]
    return topics

def getPostsByTopic(topic_id):
    if topic_id == '':
        return None
    else:
        posts = Post.objects.filter(topic_id=topic_id).order_by('created_at')

        posts = [
            {
                'id':post.id,
                'created_at':post.created_at,
                'created_by':post.created_by.username,
                'subject':post.subject,
                'message':post.message
            }
            for post
            in posts
        ]

        return posts


def getPost(post_id):
    if post_id=='' or post_id is None:
        return None
    else:
        post = Post.objects.get(id=post_id)

        {
            'created_by_user': post.created_by.username,
            'subject':post.subject

        }

    return post