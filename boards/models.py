from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)

    def get_name_url_formatted(self):
        return self.name.replace(' ', '-').lower()

    def get_name_from_url_format(url_formatted_name):
        return url_formatted_name.replace('-',' ').title()

    def get_latest_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    name_url_formatted = property(get_name_url_formatted)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=50)
    board = models.ForeignKey(Board,null=False,on_delete=models.PROTECT,related_name='topics')
    created_by = models.ForeignKey(User,null=False, on_delete=models.PROTECT, related_name='topics_created')
    updated_by = models.ForeignKey(User,null=False, on_delete=models.PROTECT, related_name='topics_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) #TODO: Should this *only* update when a user makes a post?
    views = models.PositiveIntegerField(default=0)

    def get_count_replies(self):
        if (Post.objects.filter(topic=self).count() - 1) < 0:
            return 0
        else:
            return Post.objects.filter(topic=self).count() - 1

    def get_last_post_user(self):
        if len(Post.objects.filter(topic=self)) == 0:
            return ''
        else:
            return Post.objects.filter(topic=self).order_by('-updated_by')[0].created_by.username

    def __str__(self):
        return self.subject

class Post(models.Model):
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    topic = models.ForeignKey(Topic,null=False,on_delete=models.PROTECT,related_name='topics')
    created_by = models.ForeignKey(User, null=False,on_delete=models.PROTECT, related_name='posts_created')
    updated_by = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='posts_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_reply_to = models.ForeignKey('self',null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))