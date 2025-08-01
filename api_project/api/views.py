import rest_framework.generics
from .serializers import BookSerializer
from .models import Book


# Create your views here.

class BookList(rest_framework.generics.ListAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer