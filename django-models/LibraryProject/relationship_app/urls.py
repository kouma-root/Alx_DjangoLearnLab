from django.urls import path
from . import views
from .views import LibraryDetailView
urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('LibraryDetailView/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
    