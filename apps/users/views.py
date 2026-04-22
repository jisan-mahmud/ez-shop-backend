from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from common.permissions import IsAdmin
from .utils import get_tokens
from .serializers import (
    RegisterSerializer, LoginSerializer,
    UpdateProfileSerializer, ChangePasswordSerializer,
    UserSerializer, AdminUserSerializer,
)
from .services import (
    RegisterUserService, LoginUserService,
    UpdateProfileService, ChangePasswordService,
    DeactivateUserService,
)

User = get_user_model()

# ── Auth Views ────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Register — Public or Merchant",
        request=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Validation error"),
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = RegisterUserService.run(**serializer.validated_data)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Login — all roles",
        request=LoginSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Invalid credentials"),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = LoginUserService.run(**serializer.validated_data)

        return Response({
            "user":   UserSerializer(user).data,
            "tokens": get_tokens(user),
        })


# ── Profile Views ─────────────────────────────────────────────

class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    http_method_names = ["get", "put"]
    
    def queryset(self):
        return self.request.user

    @extend_schema(
        tags=["Profile"],
        summary="Get own profile",
        responses={200: UserSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
    def get_object(self):
        return self.request.user

    @extend_schema(
        tags=["Profile"],
        summary="Update own profile",
        request=UpdateProfileSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Validation error"),
        }
    )
    def put(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UpdateProfileService.run(
            user=request.user,
            **serializer.validated_data,
        )
        return Response(UserSerializer(user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Profile"],
        summary="Change password",
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password changed"),
            400: OpenApiResponse(description="Wrong old password"),
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ChangePasswordService.run(
            user=request.user,
            **serializer.validated_data,
        )
        return Response({"message": "Password changed successfully"})


# ── Admin Views ───────────────────────────────────────────────

class AdminUserListView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminUserSerializer
    
    def get_queryset(self):
        return User.objects.exclude(is_superuser=True)

    @extend_schema(
        tags=["Admin — Users"],
        summary="List all users — Admin only",
        responses={200: AdminUserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminMerchantListView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminUserSerializer
    
    def get_queryset(self):
        return User.objects.filter(role=User.Role.MERCHANT)

    @extend_schema(
        tags=["Admin — Users"],
        summary="List all merchants — Admin only",
        responses={200: AdminUserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminDeactivateUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        tags=["Admin — Users"],
        summary="Deactivate a user — Admin only",
        responses={
            200: OpenApiResponse(description="User deactivated"),
            404: OpenApiResponse(description="User not found"),
        }
    )
    def post(self, request, user_id):
        user = DeactivateUserService.run(
            admin=request.user,
            user_id=user_id,
        )
        return Response({
            "message": f"{user.email} has been deactivated"
        })