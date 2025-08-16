from django.db import models
from django.contrib.auth.models import User

#Post model creation
class Post(models.Model):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey (User, on_delete= models.CASCADE)



#Comment model creation
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # oldest → newest (change if you prefer)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'