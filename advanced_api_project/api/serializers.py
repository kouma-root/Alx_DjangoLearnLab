from rest_framework import serializers
from .models import Book, Author


#implementing the Book Serializer importing the model and using all the fields
class BookSerializer(serializers.ModelSerializer):
    
    #implentation of the Meta method to handle the data
    class Meta:
        model = Book
        fields = '__all__'
        #Method for validate data entry to not by more than the current date
        def validate(self, data):
            pass
 
 
 #implementation of the Author serializer       
class AutrhoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ['name']