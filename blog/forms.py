from django import forms

from .models import Comment, BlogPost


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'body', 'category']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']
