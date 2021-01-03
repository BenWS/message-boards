from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=50)
    board = models.ForeignKey(Board,null=False,on_delete=models.PROTECT,related_name='topics')
    created_by = models.ForeignKey(User,null=False, on_delete=models.PROTECT, related_name='topics_created')
    updated_by = models.ForeignKey(User,null=False, on_delete=models.PROTECT, related_name='topics_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    subject = models.CharField(max_length=30)
    message = models.CharField(max_length=1000)
    topic = models.ForeignKey(Topic,null=False,on_delete=models.PROTECT,related_name='topics')
    created_by = models.ForeignKey(User, null=False,on_delete=models.PROTECT, related_name='posts_created')
    updated_by = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='posts_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_reply_to = models.ForeignKey('self',null=True, on_delete=models.PROTECT)
