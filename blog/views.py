from django.shortcuts import render

from . import models


def home(request):
    posts = models.BlogPost.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, "blog/index.html", context)
