from django.contrib import admin

from blog.models import Author, Category, Comment, BlogPost

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(BlogPost)
