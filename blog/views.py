from django.shortcuts import render

from . import models
from .forms import CommentForm
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
