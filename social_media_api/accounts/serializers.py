from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username", "email", "password", "password_confirm",
            "first_name", "last_name", "bio", "profile_picture", "token"
        )
        extra_kwargs = {
            "bio": {"required": False},
            "profile_picture": {"required": False},
        }

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        # profile_picture handled automatically if passed
        user = User.objects.create_user(**validated_data)

        # create token
        token = Token.objects.create(user=user)
        user.token = token.key  # attach dynamically for response

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")

                token, _ = Token.objects.get_or_create(user=user)
                return {"user": user, "token": token.key}
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        raise serializers.ValidationError("Must include 'username' and 'password'.")


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile_picture_url = serializers.CharField(source="profile_picture_url", read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "bio", "profile_picture_url", "date_joined",
            "followers_count", "following_count",
        )
        read_only_fields = ("id", "date_joined")

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class PublicUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "bio", "profile_picture_url",
                  "followers_count", "following_count", "is_following"]

    def get_is_following(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not (request and user and user.is_authenticated):
            return False
        return obj.followers.filter(id=user.id).exists()