from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    PublicUserSerializer,
)
from .models import CustomUser, Follow


# --- AUTHENTICATION VIEWS --- #

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return token + basic profile data.
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "token": user.token,  # Token created in serializer
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "bio": user.bio,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Authenticate user and return token + basic profile data.
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]

        # Optional: Keep session-based login (for web clients)
        login(request, user)

        return Response(
            {
                "message": "Login successful.",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "bio": user.bio,
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get or update the authenticated user's profile.
    """
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=(request.method == "PATCH"),
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout user by deleting their authentication token.
    """
    try:
        request.user.auth_token.delete()
    except (AttributeError, Token.DoesNotExist):
        pass

    return Response(
        {"message": "Successfully logged out."},
        status=status.HTTP_200_OK,
    )


# --- FOLLOW / UNFOLLOW VIEWS --- #

class FollowUserView(APIView):
    """
    Allows an authenticated user to follow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_relation, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user,
        )

        serializer = PublicUserSerializer(target_user, context={"request": request})

        return Response(
            {
                "message": "Successfully followed user." if created else "You already follow this user.",
                "followed": created,
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    """
    Allows an authenticated user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted, _ = Follow.objects.filter(
            follower=request.user,
            following=target_user,
        ).delete()

        serializer = PublicUserSerializer(target_user, context={"request": request})

        return Response(
            {
                "message": "Successfully unfollowed user." if deleted else "You were not following this user.",
                "unfollowed": bool(deleted),
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )