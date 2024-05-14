# BIM BLOG

Commission: 54140

Creator: Ai-Ling González Mac

## What is the project About
This is a blog that contains about BIM.

## Technical Description

### Git

We will use a basic form of gitflow. This means, having at least 2 branches:

- Develop: From here we will add features, and will be merged into develop.
- Main: This is the principal branch, and from here all the stable changes will be updated here.
  ![image](https://github.com/AI-LINGM/bimBlog/assets/160174361/8b3d39c5-49c3-47b6-a497-61938a7ab168)

### StartUp
`pip install -r requirements.txt`

### 🚧 First Steps:

#### 📘 Creating the Project bimBlog

First of all, start the bimBlog. So the command is the following:

`django-admin startproject bimblog .`

*Please remember to add the ending dot*

#### 📃 Creating BimBlog app

Then, we will create the main app, in this case will be the blog

`python manage.py startapp blog`

check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/1)

#### 📺 Creating the first view

In the app add the following route:

```python
from django.urls import path
from blog.views import home

urlpatterns = [
    path('', home, name='home'),
]
```

We will create a simple `base.html` so all templates can inherit from:

```html
<!DOCTYPE html>
<html lang="es">
<! –– Head Body and more stuff ––> 
<body>
    <header> </header>

    <main>
        {% block content %}{% endblock %}
    </main>
    <footer></footer>
</body>
</html>
```

In the views we will define something like this(considering that index.html inherits from base.html):

```python
from django.shortcuts import render

def home(request):
    return render(request, "blog/index.html")
```

check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/2)

#### 📐  Adding Models

For now, it will have at least 4 Main models:
1- The Author
2- The BlogPost
3- Comments.
4 - Category

It's something like this:

```python
from django.db import models


class Author(models.Model):
  # some params
  pass


class Category(models.Model):
  name = models.CharField(max_length=255)


class Comment(models.Model):
  # some params
  post = models.ForeignKey("BlogPost", on_delete=models.CASCADE)


class BlogPost(models.Model):
  # some params
  category = models.ManyToManyField(Category)
  comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
```

After adding some model, the next two steps are:

`python manage.py makemigrations`

`python manage.py migrate`

But, please do not forget to add all the models in the `admin.py` file like this:

```python
from django.contrib import admin
from blog.models import Author, Category, Comment, BlogPost

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(BlogPost)
```

And of course, If we want to manage our data, we need to be an 💸ADMIN💸, so let's do it!

`python manage.py createsuperuser`

Then we add an author, a category, and a blogpost in the admin panel, to be shown in the home as a list:
views.py

```python
def home(request):
  posts = models.BlogPost.objects.all()
  context = {
    'posts': posts,
  }
  return render(request, "blog/index.html", context)

```

index.html

```html
{% extends 'blog/base.html' %}
{% block content %}

<h2>Este es el Home</h2>
<li>
  {% for post in posts %}
  <a>{{post.title}}</a>
  {% endfor %}
</li>
{% endblock %}
```

##### check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/3)

<img width="466" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/e3425e3a-1944-4f30-a541-92dabb833d29">

#### 📺 Creating the Detail View with a first form.

If we have a blog, we should be able to see the details of the entry, and any respectable blog should have a
section comment. Let's do a comment form:

```python
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['author', 'body']
```

Let's define a view to see the detail of the blog:

**Views.py**

```python
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
```

**index.html**

```html
      {% for post in posts %}

<li>
  <a href="{% url 'post_details' post.id %}">{{ post.title }}</a>
  <p>{{ post.excerpt }}</p>

</li>
{% endfor %}
```

##### check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/4)

Home
<img width="466" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/a9a3ea60-ea9f-4bdb-bc15-3945a1ff72ea">

Details:
<img width="500" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/ed3074ed-216c-434a-88eb-a8cb3d40e5c9">

## Future Improvements

In the next deliver, this project will link the author of a blog post with an auth user.
Hopefully, registered user can Comment with their name.

## Known issues
