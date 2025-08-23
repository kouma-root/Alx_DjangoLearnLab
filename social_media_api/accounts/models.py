from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField(
        "self",
        through="Follow",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    
    def __str__(self):
        return self.username
    
    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return None
    

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_links"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower_links"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")  # prevent duplicates
        indexes = [
            models.Index(fields=["follower", "following"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.follower} -> {self.following}"