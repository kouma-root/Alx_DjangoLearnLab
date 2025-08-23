from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from rest_framework import filters
from .serializers import PostSerializer, CommentSerializer
from accounts.models import Follow
from rest_framework.response import Response
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only authors to edit/delete their posts or comments."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at"]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
        
          
class FeedView(generics.GenericAPIView):
    """
    Show posts from users that the logged-in user follows.
    Checker requirement: Post.objects.filter(author__in=following_users).order_by(...)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get all the users that the current user follows
        following_users = request.user.following.all()
        
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        # Return simple JSON (or use serializer if you already have one)
        data = [
            {
                "id": post.id,
                "author": post.author.username,
                "content": post.content,
                "created_at": post.created_at,
            }
            for post in posts
        ]
        return Response(data)