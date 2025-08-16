from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
                    PostCreateView, PostDetailView, PostListView, PostDeleteView, PostUpdateView, register, profile)


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name= 'blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page= 'login'), name= 'logout'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]