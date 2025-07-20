from django.urls import path
from . import views
from .views import library_detail

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('library_detail/<int:pk>/', library_detail.as_view(), name='library_detail'),
]
    