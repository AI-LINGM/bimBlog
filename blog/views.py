import random
import re

from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import CommentForm, CreateBlogPostForm, SearchForm, UpdateBlogPostForm, CustomAuthenticationForm, \
    CustomUserCreationForm
from .models import BlogPost, Category, Comment


def home(request):
    posts = models.BlogPost.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'categories': categories
    }
    return render(request, "blog/index.html", context)


def blog_post_detail(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        random_quote = select_random_quote(post.body)

    except ObjectDoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            comments = Comment.objects.filter(post=post)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'random_quote': random_quote,

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


def update_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = UpdateBlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = UpdateBlogPostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'blog/update_post.html', context)


def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect("home")
    context = {'post': post}
    return render(request, 'blog/delete_post.html', context)


class LoginBlogView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "blog/login.html"


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            form.save()
            return render(request, "blog/index.html", {"mensaje": f"Usuario '{username}' creado"})
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


def pages(request):
    posts = models.BlogPost.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, "blog/pages.html", context)


def about(request):
    return render(request, "blog/about.html")


def select_random_quote(paragraph):
    sentences = re.split(r'(?<=[.!?]) +', paragraph)

    random_quote = random.choice(sentences)

    return random_quote
