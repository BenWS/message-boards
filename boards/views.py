from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.db.models import F, CharField, Value
from boards.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from urllib.parse import urlparse

from boards.view_helpers import *
from boards import view_helpers


def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html'
                  , context={'boards': boards, 'home_page': True})


def topics(request, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topics = view_helpers.getTopicsByBoard(board.id)
    context = {
        'topics': topics
        , 'board_name_url_formatted': board.name_url_formatted
        , 'board_name': board.name
    }
    return render(request, 'boards/topics.html', context=context)


def viewTopic(request, topic_id, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topic = get_object_or_404(Topic, id=topic_id)
    posts = getPostsByTopic(topic_id)
    context = {
        'posts': posts,
        'topic': topic,
        'board': board
    }

    return render(request, 'boards/view-topic.html', context=context)


def createTopic(request, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    if request.method == 'GET':
        context = {
            'current_username': request.user.username,
            'board_name': board.name,
            'board_name_url_formatted': board.name_url_formatted
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
        return HttpResponseRedirect(reverse('boards:topics', kwargs={'board_name': board.name_url_formatted}))


def createPost(request, board_name, topic_id):
    board_name = board_name.replace('-', ' ')
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topic = get_object_or_404(Topic, id=topic_id)

    # http://localhost:8000/boards/hiking-locations/topic/3/create-post?post_id=2
    if request.method == 'GET':
        # NOTE: there should be handling for an attempt to reply to a post not in topic

        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse('boards:login'))

        in_reply_to_post = view_helpers.getPost(view_helpers.getQueryDictItem(request, 'post_id'))

        context = {
            'current_username': request.user.username,
            'post': in_reply_to_post,
            'board_name': board_name,
            'board_name_url_formatted': board.name_url_formatted,
            'topic': topic
        }

        return render(request, 'boards/create-post.html', context=context)

    if request.method == 'POST':

        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        current_topic_posts = [post['id'] for post in view_helpers.getPostsByTopic(topic_id)]
        in_reply_to_post = view_helpers.getPost(view_helpers.getQueryDictItem(request, 'post_id'))

        if in_reply_to_post is not None \
                and in_reply_to_post.id not in current_topic_posts:
            return HttpResponse('Not Acceptable', status=406)

        Post.objects.create(
            subject=request.POST['subject'],
            message=request.POST['message'],
            created_by_id=request.user.id,
            updated_by_id=request.user.id,
            in_reply_to=in_reply_to_post,
            topic_id=topic_id
        )

        return HttpResponseRedirect(
            reverse('boards:view-topic', kwargs={'topic_id': topic_id, 'board_name': board_name}))


def editPost(request, board_name, topic_id, post_id):
    topic = get_object_or_404(Topic, id=topic_id)
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    post = get_object_or_404(Post, id=post_id)
    in_reply_to_post = None if post.in_reply_to is None else Post.objects.get(id=post.in_reply_to)

    post_topic = post.topic
    post_board = post_topic.board

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('boards:login'))

    if board != post_board or topic != post_topic:
        return HttpResponseBadRequest('Bad Request - post does not belong to topic or board provided')

    if post.created_by != request.user:
        return HttpResponseForbidden('User does not have permission to edit this post')

    context = {
        'current_username': request.user.username,
        'board_name': board.name,
        'board_name_url_formatted': board.name_url_formatted,
        'topic': topic,
        'post': post,
        'in_reply_to_post_creator': in_reply_to_post.created_by.username if post.in_reply_to else None,
        'in_reply_to_post_subject': in_reply_to_post.subject if post.in_reply_to else None
    }
    if request.method == 'GET':
        return render(request, 'boards/edit-post.html', context)

    if request.method == 'POST':
        post.message = request.POST['message']
        post.subject = request.POST['subject']
        post.save()

        return HttpResponseRedirect(
            reverse('boards:view-topic', kwargs={'board_name': board.name_url_formatted, 'topic_id': topic_id}))


def contactAdmin(request):
    return render(request, 'boards/contact-site-admin.html')


def userSignup(request):
    if request.method == 'GET':
        return render(request, 'boards/sign-up.html')
    elif request.method == 'POST':
        len_users_username = len(User.objects.filter(username=request.POST['username']))
        len_users_email = len(User.objects.filter(username=request.POST['email']))

        if len_users_username > 0 or len_users_email > 0:
            error = 'Username or email already associated with existing account'
            return render(request,'boards/sign-up.html', context={'error':error})

        else:
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )

            return HttpResponseRedirect(reverse('boards:index'))


def userLogin(request):
    if request.method == 'GET':
        return render(request, 'boards/login.html')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('boards:index'))
        else:
            error_string = 'Invalid username or password. Please try again.'
            return render(request, 'boards/login.html',context={'error_string':error_string})


def userLogoff(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('boards:index'))
