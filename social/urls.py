from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]