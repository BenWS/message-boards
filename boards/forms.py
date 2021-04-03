from django import forms
from boards.models import Topic, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class CreateTopicForm(forms.ModelForm):
    message = forms.CharField(label='Message'
                              , widget=forms.Textarea
                              , max_length=1000
                              )

    class Meta:
        model = Topic
        fields = ['subject','message']

class CreatePostForm(forms.ModelForm):
    in_reply_to_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    message = forms.CharField(widget=forms.Textarea, max_length = 1000)

    class Meta:
        model = Post
        fields = ['subject','message','in_reply_to_id']

class EditPostForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, max_length=1000)

    class Meta:
        model = Post
        fields = ['subject','message']