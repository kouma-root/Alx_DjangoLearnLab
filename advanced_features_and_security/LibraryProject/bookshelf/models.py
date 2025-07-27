from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ('can_view', 'Can view book details'),
            ('can_create', 'Can create a new book'),
            ('can_edit', 'Can edit book details'),
            ('can_delete', 'Can delete book'),
        ]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user  
    
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank= True)
    profile_photo = models.ImageField(upload_to='profiles/', null= True, blank= True)
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username