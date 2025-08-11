from django.db import models

# Create your models here.
#implementing model for the author
class Author(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return self.name
    
#Implementing method for book and using author as a foreign key    
class Book(models.Model):
    title = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    
    def __str__(self) -> str:
        return self.title