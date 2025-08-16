from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
                    PostCreateView, PostDetailView, PostListView, PostDeleteView, PostUpdateView, register, profile,
                     CommentListView, CommentCreateView, CommentUpdateView, CommentDeleteView)


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name= 'blog/login.html', next_page = 'profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page= 'login'), name= 'logout'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:post_id>/comments/", CommentListView.as_view(), name="comment-list"),
    path("post/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]