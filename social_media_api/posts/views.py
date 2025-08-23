from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from rest_framework import filters
from .serializers import PostSerializer, CommentSerializer

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
        
        
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()  # users I follow
        qs = Post.objects.filter(author__in=followed_users).order_by("-created_at")
        # Optional: include your own posts if ?include_self=true
        include_self = self.request.query_params.get("include_self") == "true"
        if include_self:
            qs = qs | Post.objects.filter(author=user)
        return qs.order_by("-created_at")