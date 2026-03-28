

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.all_posts, name='all_posts'),
    path('stories/', views.all_stories, name='all_stories'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('story/', views.create_story, name='create_story'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('react/<int:id>/', views.react_post, name='react_post'),
    path('comment/<int:id>/', views.add_comment, name='add_comment'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('edit/<int:id>/', views.edit_post, name='edit_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
]