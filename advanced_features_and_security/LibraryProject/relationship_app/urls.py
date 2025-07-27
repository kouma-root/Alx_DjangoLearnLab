from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books
from .views import LibraryDetailView
urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('LibraryDetailView/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),
    path('<int:pk>/edit_book/', views.update_book, name='update_book'),
    path('<int:pk>/delete_book/', views.delete_book, name='delete_book'),
]
    