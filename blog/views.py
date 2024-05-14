from django.shortcuts import render, redirect

from . import models
from .forms import CommentForm, CreateBlogPostForm
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
