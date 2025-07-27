from django.urls import path
from .views import book_list, book_create, book_edit, book_delete
urlpatterns = [
    path('', book_list, name='book_list'),
    path('create/', book_create, name='book_create'),
    path('edit/<int:pk>/', book_edit, name='book_edit'),
    path('delete/<int:pk>/', book_delete, name='book_delete'),
]