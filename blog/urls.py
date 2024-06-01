from django.contrib.auth.views import LogoutView
from django.urls import path

from blog.views import home, blog_post_detail, create_blog_post, search, update_post, delete_post, LoginBlogView, \
    register, pages, about

urlpatterns = [
    path('', home, name='home'),
    path('post/details/<int:pk>', blog_post_detail, name='post_details'),
    path('create_post/', create_blog_post, name='create_post'),
    path('search/', search, name='search'),
    path('update_post/<int:pk>/', update_post, name='update_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
    path('pages', pages, name='pages'),
    path('login', LoginBlogView.as_view(), name='login'),
    path('logout', LogoutView.as_view(template_name='blog/logout.html'), name="logout"),
    path("register", register, name="register"),
    path("about", about, name="about"),
]
