from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)

    def get_name_url_formatted(self):
        return self.name.replace(' ', '-').lower()

    def get_name_from_url_format(url_formatted_name):
        return url_formatted_name.replace('-',' ').title()

    name_url_formatted = property(get_name_url_formatted)

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
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    topic = models.ForeignKey(Topic,null=False,on_delete=models.PROTECT,related_name='topics')
    created_by = models.ForeignKey(User, null=False,on_delete=models.PROTECT, related_name='posts_created')
    updated_by = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='posts_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_reply_to = models.ForeignKey('self',null=True, on_delete=models.PROTECT)
