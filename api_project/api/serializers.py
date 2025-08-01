import rest_framework.serializers
from .models import Book


class BookSerializer(rest_framework.serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'