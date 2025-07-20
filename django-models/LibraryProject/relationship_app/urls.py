from django.urls import path
from . import views
from .views import library_detail

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('library_detail/<int:pk>/', library_detail.as_view(), name='library_detail'),
]
    