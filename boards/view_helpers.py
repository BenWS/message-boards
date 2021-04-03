from boards.models import *
from datetime import datetime, timezone
from django.db.models import Max


temporary_user_id = 1

def getQueryDictItem(request, key):
    #NOTE: I should include handling for POST and other methods as well
    try:
        return request.GET[key]
    except KeyError:
        try:
            return request.POST[key]
        except KeyError:
            return None

def safe_list_get(list,index):
    try:
        return list[index]
    except IndexError:
        return None

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