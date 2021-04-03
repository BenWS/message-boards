from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import now


from boards.models import *
from boards.forms import \
    CreateTopicForm, \
    CreatePostForm, \
    EditPostForm

from boards.view_helpers import *
from boards import view_helpers

class BoardListView(ListView):
    model=Board
    context_object_name='boards'
    template_name='boards/boards.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board_name_url_formatted'] = self.board.name_url_formatted
        kwargs['board_name'] = self.board.name
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board,name=Board.get_name_from_url_format(self.kwargs['board_name']))
        queryset = Topic.objects.filter(board=self.board).order_by('-updated_at')
        return queryset

def topics(request, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    topics_queryset = view_helpers.getTopicsByBoard(board.id)
    page = request.GET.get('page',1)
    paginator = Paginator(topics_queryset, 10)

    #TODO: Provide descending order to topics on individual page

    topics = paginator.get_page(page)

    context = {
        'topics': topics
        , 'board_name_url_formatted': board.name_url_formatted
        , 'board_name': board.name
    }

    return render(request, 'boards/topics.html', context=context)

#TODO: Delete old view functions that have been replaced by GCBV
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/view-topic.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['current_user'] = self.request.user.username
        kwargs['topic'] = self.topic
        kwargs['board'] = self.topic.board
        kwargs['post_original'] = self.post_original
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #TODO: Research: does this always execute before get_context_data?
        board_name = self.kwargs['board_name']
        topic_id = self.kwargs['topic_id']
        self.topic = get_object_or_404(Topic,board__name=Board.get_name_from_url_format(board_name), id=topic_id)
        self.topic.views += 1
        self.topic.save()
        queryset = Post.objects.filter(topic=self.topic).order_by('updated_at')
        self.post_original = view_helpers.safe_list_get(queryset,0)
        print(queryset)
        return queryset

def viewTopic(request, topic_id, board_name):
    topic = get_object_or_404(Topic, board__name=Board.get_name_from_url_format(board_name),id=topic_id)
    topic.views += 1
    topic.save()
    context = {
        'current_user':request.user.username,
        'topic': topic,
        'board': topic.board
    }

    return render(request, 'boards/view-topic.html', context=context)


@login_required
def createTopic(request, board_name):
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))

    form = CreateTopicForm()

    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
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

@login_required
def createPost(request, board_name, topic_id):
    board_name = board_name.replace('-', ' ')
    topic = get_object_or_404(Topic, board__name=Board.get_name_from_url_format(board_name),id=topic_id)
    recent_posts = Post.objects.filter(topic=topic).order_by('-created_at')[0:4]

    in_reply_to_post = view_helpers.getPost(view_helpers.getQueryDictItem(request, 'post_id'))
    if in_reply_to_post is not None:
        form = CreatePostForm(initial={'in_reply_to_id':in_reply_to_post.id})
    else:
        form = CreatePostForm()

    if request.method=='GET':
        context = {
            'board_name': board_name,
            'board_name_url_formatted': board_name,
            'topic': topic,
            'form': form,
            'recent_posts': recent_posts
        }

        return render(request, 'boards/create-post.html', context=context)


    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            current_topic_posts = [post.id for post in Post.objects.filter(topic__id=topic_id)]

            if in_reply_to_post is not None \
                    and in_reply_to_post.id not in current_topic_posts:
                return HttpResponse('Not Acceptable', status=406)

            post = form.save(commit=False)
            post.created_by = request.user
            post.updated_by = request.user
            post.topic = topic
            post.topic.updated_at = now()
            topic.save()
            post.save()

            return HttpResponseRedirect(
                reverse('boards:view-topic', kwargs={'topic_id': topic_id, 'board_name': board_name}))
        else:
            context = {
                'board_name': board_name,
                'board_name_url_formatted': board_name,
                'topic': topic,
                'form': form,
                'recent_posts': recent_posts
            }
            return render(request, 'boards/create-post.html', context=context)

def editPost(request, board_name, topic_id, post_id):
    topic = get_object_or_404(Topic, id=topic_id)
    board = get_object_or_404(Board, name=Board.get_name_from_url_format(board_name))
    post = get_object_or_404(Post, id=post_id)
    in_reply_to_post = None if post.in_reply_to is None else Post.objects.get(id=post.in_reply_to.id)

    post_topic = post.topic
    post_board = post_topic.board

    form = EditPostForm(initial={'subject':post.subject, 'message':post.message})

    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('accounts:login'))

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
