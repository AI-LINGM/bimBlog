from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} '{self.last_name}'"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("BlogPost", on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f"{self.author} on '{self.body}'"


class BlogPost(models.Model):
    image = models.ImageField(upload_to='images/', default='default_image_blog')
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title
