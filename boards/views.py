from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.db.models import F, CharField, Value
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from urllib.parse import urlparse

from boards.models import *
from boards.forms import \
    CreateTopicForm, \
    CreatePostForm, \
    EditPostForm, \
    UserLoginForm

from boards.view_helpers import *
from boards import view_helpers


def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html'
                  , context={'boards': boards, 'home_page': True})


def topics(request, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topics = view_helpers.getTopicsByBoard(board.id)
    print('PRINTING...')
    # print([topic['id'] for topic in topics])
    print(board.name)
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

    form = CreateTopicForm()

    if request.user.is_anonymous:
        response = HttpResponseRedirect(reverse('boards:login'))
        return response

    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        if form.is_valid():
            created_topic = Topic.objects.create(
                board=board,
                subject=form.cleaned_data.get('subject'),
                created_by_id=request.user.id,
                updated_by_id=request.user.id
            )

            Post.objects.create(
                created_by_id=request.user.id,
                updated_by_id=request.user.id,
                topic=created_topic,
                subject=form.cleaned_data.get('subject'),
                message=form.cleaned_data.get('message')
            )
            return HttpResponseRedirect(reverse('boards:topics', kwargs={'board_name': board.name_url_formatted}))


    context = {
        'current_username': request.user.username,
        'board_name': board.name,
        'board_name_url_formatted':board.name_url_formatted,
        'form': form
    }

    return render(request,'boards/create-topic.html', context=context)


def createPost(request, board_name, topic_id):
    board_name = board_name.replace('-', ' ')
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topic = get_object_or_404(Topic, id=topic_id)

    # http://localhost:8000/boards/hiking-locations/topic/3/create-post?post_id=2

    in_reply_to_post = view_helpers.getPost(view_helpers.getQueryDictItem(request, 'post_id'))
    if in_reply_to_post is not None:
        form = CreatePostForm(initial={'in_reply_to_id':in_reply_to_post.id})
    else:
        form = CreatePostForm()

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('boards:login'))

    context = {
        'board_name': board_name,
        'board_name_url_formatted': board.name_url_formatted,
        'topic': topic,
        'form': form
    }

    if request.method == 'POST':

        form = CreatePostForm(request.POST)

        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        if form.is_valid():
            current_topic_posts = [post['id'] for post in view_helpers.getPostsByTopic(topic_id)]

            if in_reply_to_post is not None \
                    and in_reply_to_post.id not in current_topic_posts:
                return HttpResponse('Not Acceptable', status=406)

            post = form.save(commit=False)
            post.created_by = request.user
            post.updated_by = request.user
            post.topic = topic
            post.save()

            return HttpResponseRedirect(
                reverse('boards:view-topic', kwargs={'topic_id': topic_id, 'board_name': board_name}))

    return render(request, 'boards/create-post.html', context=context)

def editPost(request, board_name, topic_id, post_id):
    topic = get_object_or_404(Topic, id=topic_id)
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    post = get_object_or_404(Post, id=post_id)
    in_reply_to_post = None if post.in_reply_to is None else Post.objects.get(id=post.in_reply_to.id)

    post_topic = post.topic
    post_board = post_topic.board

    form = EditPostForm({'subject':post.subject, 'message':post.message})

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('boards:login'))

    if board != post_board or topic != post_topic:
        return HttpResponseBadRequest('Bad Request - post does not belong to topic or board provided')

    if post.created_by != request.user:
        return HttpResponseForbidden('User does not have permission to edit this post')

    if request.method == 'POST':
        form = EditPostForm(request.POST)

        if form.is_valid():
            post.subject = request.POST['subject']
            post.message = request.POST['message']
            post.save()
            return HttpResponseRedirect(
                reverse('boards:view-topic', kwargs={'board_name': board.name_url_formatted, 'topic_id': topic_id}))

    context = {
        'current_username': request.user.username,
        'board_name': board.name,
        'board_name_url_formatted': board.name_url_formatted,
        'topic': topic,
        'post': post,
        'in_reply_to_post_creator': in_reply_to_post.created_by.username if post.in_reply_to else None,
        'in_reply_to_post_subject': in_reply_to_post.subject if post.in_reply_to else None,
        'form': form
    }

    return render(request, 'boards/edit-post.html', context)


def contactAdmin(request):
    return render(request, 'boards/contact-site-admin.html')

def userLogin(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('boards:index'))

    print("Failed!")
    return render(request, 'boards/login.html',context={'form':form})


def userLogoff(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('boards:index'))
