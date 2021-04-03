from django.contrib.auth.models import User
from boards.models import Board, Topic, Post

user = User.objects.first()

board = Board.objects.get(name='Equipment')

for i in range(100):
    subject = 'Topic test #{}'.format(i)
    topic = Topic.objects.create(subject=subject, board=board, created_by=user, updated_by=user)
    Post.objects.create(subject='Lorem ipsum...',message='Lorem ipsum...', topic=topic, created_by=user, updated_by=user)