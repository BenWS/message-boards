from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.db.models import F, CharField, Value
from boards.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from urllib.parse import urlparse

from boards.view_helpers import *
from boards import view_helpers

def home(request):
    boards = Board.objects.all().values()
    for board in boards:
        print(board)
        board['name_urlFormatted'] = board['name'].replace(' ','-').lower()
    return render(request,'boards/boards.html'
                  , context={'boards':boards, 'home_page':True})

def topics(request, board_name):
    board_name_urlFormatted = board_name
    board_name = board_name.replace('-', ' ')
    board_id = get_object_or_404(Board, name=board_name).id
    topics = view_helpers.getTopicsByBoard(board_id)
    context = {
        'topics':topics
        , 'board_name_urlFormatted': board_name_urlFormatted
        , 'board_name': board_name
    }
    return render(request, 'boards/topics.html', context=context)

def viewTopic(request, topic_id, board_name):
    board_name = board_name.replace('-', ' ')
    print("Breakpoint reached")
    board = get_object_or_404(Board,name=board_name)
    topic = get_object_or_404(Topic, id=topic_id)
    posts = getPostsByTopic(topic_id)
    board = topic.board.__dict__
    board['name_urlFormatted'] = board['name'].replace(' ', '-').lower()
    context = {
        'posts':posts,
        'topic':topic,
        'board':board
    }

    return render(request,'boards/view-topic.html',context=context)

def createTopic(request,board_name):
    board_name_urlFormatted = board_name
    board_name = board_name.replace('-', ' ')
    if request.method == 'GET':
        context = {
            'current_username':request.user.username,
            'board_name':board_name,
            'board_name_urlFormatted': board_name.replace(' ','-')
        }

        if request.user.is_anonymous:
            response = HttpResponseRedirect(reverse('boards:login'))
            return response
        else:
            return render(request, 'boards/create-topic.html', context=context)



    if request.method == 'POST':
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)
        created_topic = Topic.objects.create(
            board=Board.objects.get(name=board_name),
            subject=request.POST['subject'],
            created_by_id=request.user.id,
            updated_by_id=request.user.id
        )

        Post.objects.create(
            created_by_id=request.user.id,
            updated_by_id=request.user.id,
            topic=created_topic,
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        return HttpResponseRedirect(reverse('boards:topics',kwargs={'board_name':board_name_urlFormatted}))

def createPost(request,board_name, topic_id):
    board_name = board_name.replace('-', ' ')
    board = get_object_or_404(Board, name=board_name)
    topic = get_object_or_404(Topic, id=topic_id)

    #http://localhost:8000/boards/hiking-locations/topic/3/create-post?post_id=2
    if request.method == 'GET':
        #NOTE: there should be handling for an attempt to reply to a post not in topic
        context= {
            'current_username':request.user.username,
            'post':view_helpers.getPost(view_helpers.getQueryDictItem(request,'post_id')),
            'board_name': board_name,
            'board_name_urlFormatted': board_name.replace(' ','-'),
            'topic':topic
        }

        return render(request, 'boards/create-post.html', context=context)

    if request.method == 'POST':
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        Post.objects.create(
            subject=request.POST['subject'],
            message=request.POST['message'],
            created_by_id = request.user.id,
            updated_by_id = request.user.id,
            topic_id = topic_id
        )

        return HttpResponseRedirect(reverse('boards:view-topic', kwargs={'topic_id':topic_id,'board_name':board_name}))

def editPost(request, board_name, topic_id, post_id):
    board_name_urlFormatted = board_name
    board_name = board_name.replace('-', ' ')
    topic = Topic.objects.get(id=topic_id)
    board = Board.objects.get(name=board_name)
    post = Post.objects.get(id=post_id)
    in_reply_to_post = None if post.in_reply_to is None else Post.objects.get(id=post.in_reply_to)

    context = {
        'current_username':User.objects.get(id=request.user.id).username,
        'board_name':board_name,
        'board_name_urlFormatted':board_name,
        'topic': topic,
        'post':post,
        'in_reply_to_post_creator':in_reply_to_post.created_by.username if post.in_reply_to else None,
        'in_reply_to_post_subject': in_reply_to_post.subject if post.in_reply_to else None
    }
    if request.method == 'GET':
        return render(request, 'boards/edit-post.html', context)

    if request.method == 'POST':
        post.message = request.POST['message']
        post.subject = request.POST['subject']
        post.save()

        return HttpResponseRedirect(reverse('boards:view-topic',kwargs={'board_name':board_name_urlFormatted, 'topic_id':topic_id}))

def contactAdmin(request):
    return render(request,'boards/contact-site-admin.html')

def userSignup(request):
    if request.method == 'GET':
        return render(request, 'boards/sign-up.html')
    elif request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return HttpResponseRedirect(reverse('boards:index'))


def userLogin(request):
    print("Hello world!")
    referring_url = print(request.META['HTTP_REFERER'])
    parsed_referring_url = urlparse(referring_url)
    referring_path = parsed_referring_url.path

    if request.method == 'GET':
        return render(request,'boards/login.html')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
        return HttpResponseRedirect(reverse('boards:index'))

def userLogoff(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('boards:index'))