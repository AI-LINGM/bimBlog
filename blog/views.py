from django.db.models import Q
from django.shortcuts import render, redirect

from . import models
from .forms import CommentForm, CreateBlogPostForm, SearchForm
from .models import BlogPost


def home(request):
    posts = models.BlogPost.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, "blog/index.html", context)


def blog_post_detail(request, pk):
    post = BlogPost.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
    }
    return render(request, "blog/post_details.html", context)


def create_blog_post(request):
    if request.method == 'POST':
        form = CreateBlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_details', pk=form.instance.pk)
    else:
        form = CreateBlogPostForm()
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)


def search(request):
    posts = ""

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            author = form.cleaned_data['author']
            category = form.cleaned_data['category']
            posts = BlogPost.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            if author:
                posts = posts.filter(author=author)
            if category:
                posts = posts.filter(category=category)
    else:
        form = SearchForm()
    context = {'form': form, 'posts': posts}
    return render(request, 'blog/search.html', context)
