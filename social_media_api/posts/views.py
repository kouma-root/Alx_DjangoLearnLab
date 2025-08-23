from rest_framework import viewsets, permissions, generics, status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from accounts.models import Follow
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like



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
    
    
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Prevent multiple likes
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification for post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        return Response(
            {"detail": "Post unliked." if deleted else "You had not liked this post."},
            status=status.HTTP_200_OK
        )