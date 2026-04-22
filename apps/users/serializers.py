# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    phone    = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")
    role     = serializers.ChoiceField(
        choices=["merchant"],   # public cannot self-register as admin
        required=False,
        allow_blank=True,
        default="",
    )
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    phone = serializers.CharField(max_length=20,  required=False, allow_blank=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)



class UserSerializer(serializers.ModelSerializer):
    """Basic profile — returned after login/register."""
    class Meta:
        model  = User
        fields = ["id", "email", "username", "phone", "role"]


class AdminUserSerializer(serializers.ModelSerializer):
    """Admin sees full user details."""
    class Meta:
        model  = User
        fields = ["id", "email", "username", "phone", "role",
                  "is_active", "date_joined", "last_login"]