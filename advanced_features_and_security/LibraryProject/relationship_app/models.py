from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    role = models.CharField(max_length=20, choices=[('admin','Admin'),('librarian','Librarian'),('member','Member')], default='member')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created :
        UserProfile.objects.create(user = instance)
    else :
        instance.userprofile.save()
