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
## Future Improvements

## Known issues
