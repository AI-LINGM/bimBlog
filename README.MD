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

#### 📺 Create Blog View.

It is a little boring to add blog by hand in the admin panel. Eventually, we want that any registered user can create
post.
Only them should create post. For now, it will be open for everyone. So lets add a button in the `index.html`

```html
{% extends 'blog/base.html' %}
{% block content %}

<h2>Este es el Home</h2>

<ul>
  {% for post in posts %}

  <li>
    <a href="{% url 'post_details' post.id %}">{{ post.title }}</a>
    <p>{{ post.body|truncatechars:200}}</p>

  </li>
  {% endfor %}

  <button onclick="location.href={% url 'create_post' %}" type="button">Create a New Post</button>

</ul>
{% endblock %}
```

Add de form Logic:

##### forms.py

```python
class CreateBlogPostForm(forms.ModelForm):
  class Meta:
    model = BlogPost
    fields = ['title', 'author', 'body', 'category']
```

##### views.py

After creation, it will be redirected to the corresponding details.

```python
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
```

##### New Button in home

<img width="400" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/d136794d-9902-4e15-b4e3-29bb14befee7">

##### Adding a new Post

<img width="400" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/9be105c5-f971-4aa5-9504-9dae1e7005d0">

##### Redirection to Post Details after creation

<img width="400" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/4fdadd02-793f-4f4c-a28d-bcee2960a19e">

##### Home with the new post

<img width="452" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/58fba659-fdcc-4407-8b41-18c286f033c5">

##### check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/5)

#### 📺 Create Search View.

Let's implement a search view, just a simple search by content, or author or even category:

##### forms.py

```python
class SearchForm(forms.Form):
  query = forms.CharField(label="Search", max_length=100, required=False)
  author = forms.ModelChoiceField(label="Author", queryset=Author.objects.all(), required=False)
  category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), required=False)
```

##### views.py

```python
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
```

Now we can see some examples, like not founding anything, searching for title or even filter by author or category.

<img width="452" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/de395898-ad12-45e6-8c4d-ed20ab18e944">

<img width="471" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/bed7f7b4-d916-4948-8e78-0cf3401429a1">

<img width="471" alt="image" src="https://github.com/AI-LINGM/bimBlog/assets/160174361/786b790c-fd26-4159-9d13-854c137f062d">

##### check these step in this [PR](https://github.com/AI-LINGM/bimBlog/pull/6

## Future Improvements

In the next deliver, this project will link the author of a blog post with an auth user.
Hopefully, registered user can Comment with their name.
Eventually, we want that any registered user can create post.
Only them should create post. For now, it will be open for everyone

## Known issues
