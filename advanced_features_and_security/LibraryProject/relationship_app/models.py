from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .managers import CustomUserManager
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book"),
            ("can_change_book", "Can change book details"),
            ("can_delete_book", "can delete a book"),
        ]
    
    def __str__(self) -> str:
        return f"({self.title} , {self.author})"
    
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)
    
    def __str__(self) -> str:
        return f"({self.name} , {self.books})"
    

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete= models.CASCADE)
    
    def __str__(self) -> str:
        return f"({self.name} , {self.library})"
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank= True)
    role = models.CharField(max_length=20, choices=[('admin','Admin'),('librarian','Librarian'),('member','Member')], default='member')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'role']

    objects = CustomUserManager()
   
    def __str__(self):
       return self.email