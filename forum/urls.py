from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    like_post,
)

urlpatterns = [
    path('', views.index, name ='user-home'),
    path('post/<int:pk>/', views.post_detail, name ='post-detail'),
    path('like/', views.like_post, name ='like_post_url'),
    path('post/new/', PostCreateView.as_view(), name ='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('notifications/' , views.notifications, name = 'notifications'),
]
