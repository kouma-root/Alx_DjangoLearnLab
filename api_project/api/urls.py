from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls))
]