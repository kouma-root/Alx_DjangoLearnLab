from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .serializers import BookSerializer
from .models import Book


# Create your views here.

class BookList(generics.ListAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
    
class BookViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer