from django.urls import path
from . import views
from .views import Library_detail

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('Library_detail/<int:pk>/', Library_detail.as_view(), name='library_detail'),
]
    