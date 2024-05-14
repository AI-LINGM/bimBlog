from django.urls import path

from blog.views import home, blog_post_detail, create_blog_post

urlpatterns = [
    path('', home, name='home'),
    path('post/details/<int:pk>', blog_post_detail, name='post_details'),
    path('create_post/', create_blog_post, name='create_post'),
]
