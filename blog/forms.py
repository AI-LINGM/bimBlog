from django import forms

from .models import Comment, BlogPost, Author, Category


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


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100, required=False)
    author = forms.ModelChoiceField(label="Author", queryset=Author.objects.all(), required=False)
    category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), required=False)
