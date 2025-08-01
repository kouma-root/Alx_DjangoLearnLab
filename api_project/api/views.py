from rest_framework.generics import ListAPIView
from .serializers import BookSerializer
from .models import Book


# Create your views here.

class BookList(ListAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer