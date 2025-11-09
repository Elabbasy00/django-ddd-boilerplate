"""
Presentation layer: API views using DDD application services.
"""

from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth import password_validation

from src.api.mixins import ApiAuthMixin
from src.infrastructure.dependency_injection.container import get_container
from src.application.shared.dtos import UserCreateDTO, UserUpdateDTO
from src.application.shared.exceptions import ApplicationError, NotFoundError, ConflictError


class CreateUser(AllowAny, APIView):
    """
    API endpoint for user registration.
    Uses CreateUserUseCase from application layer.
    """

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, allow_blank=True)
        last_name = serializers.CharField(required=False, allow_blank=True)
        username = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container = get_container()
        use_case = container.create_user_use_case

        user_dto = use_case.execute(
            UserCreateDTO(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
            )
        )
        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user_dto.id,
                    "username": user_dto.username,
                    "email": user_dto.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class UserSessionLoginApi(AllowAny, APIView):
    """
    API endpoint for session-based login.
    Uses AuthenticateUserUseCase from application layer.
    """

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container = get_container()
        use_case = container.authenticate_user_use_case

        auth_result = use_case.execute(
            username=serializer.validated_data["username"], password=serializer.validated_data["password"]
        )

        if auth_result is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get Django user for session login
        from src.users.models import User as DjangoUser

        django_user = DjangoUser.objects.get(id=auth_result.user.id)
        login(request, django_user)

        session_key = request.session.session_key

        return Response(
            {
                "session": session_key,
                "data": {
                    "id": auth_result.user.id,
                    "email": auth_result.user.email,
                    "is_active": auth_result.user.is_active,
                    "is_admin": auth_result.user.is_admin,
                    "is_superuser": auth_result.user.is_superuser,
                },
            }
        )


class UserSessionLogoutApi(ApiAuthMixin, APIView):
    """API endpoint for session-based logout."""

    def get(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})


class UserJwtLoginApi(TokenObtainPairView):
    """
    API endpoint for JWT-based login.
    Uses AuthenticateUserJWTUseCase from application layer.
    """

    def post(self, request, *args, **kwargs):
        # Use the base TokenObtainPairView for JWT token generation
        # This integrates with Django's authentication system
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        # Set JWT cookie if configured
        if settings.SIMPLE_JWT.get("JWT_AUTH_COOKIE") is not None:
            response.set_cookie(
                key=settings.SIMPLE_JWT["JWT_AUTH_COOKIE"],
                value=response.data.get("access"),
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT.get("JWT_AUTH_COOKIE_SECURE", False),
                samesite=settings.SIMPLE_JWT.get("JWT_AUTH_COOKIE_SAMESITE", "Lax"),
            )

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    """API endpoint for JWT-based logout."""

    def post(self, request):
        response = Response({"message": "Logged out successfully"})

        if settings.SIMPLE_JWT.get("JWT_AUTH_COOKIE") is not None:
            response.delete_cookie(settings.SIMPLE_JWT["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    """
    API endpoint for getting/updating current user profile.
    Uses GetUserUseCase and UpdateUserUseCase from application layer.
    """

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, allow_blank=True)
        last_name = serializers.CharField(required=False, allow_blank=True)
        email = serializers.EmailField(required=False)

    def get(self, request):
        """Get current user profile."""
        container = get_container()
        use_case = container.get_user_use_case

        try:
            user_dto = use_case.execute(user_id=request.user.id)
            return Response(
                {
                    "id": user_dto.id,
                    "email": user_dto.email,
                    "username": user_dto.username,
                    "first_name": user_dto.first_name,
                    "last_name": user_dto.last_name,
                    "is_active": user_dto.is_active,
                    "is_admin": user_dto.is_admin,
                    "is_superuser": user_dto.is_superuser,
                }
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Update current user profile."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        container = get_container()
        use_case = container.update_user_use_case

        try:
            user_dto = use_case.execute(
                user_id=request.user.id,
                user_data=UserUpdateDTO(
                    first_name=serializer.validated_data.get("first_name"),
                    last_name=serializer.validated_data.get("last_name"),
                    email=serializer.validated_data.get("email"),
                ),
            )
            return Response(
                {
                    "id": user_dto.id,
                    "email": user_dto.email,
                    "username": user_dto.username,
                    "first_name": user_dto.first_name,
                    "last_name": user_dto.last_name,
                    "is_active": user_dto.is_active,
                    "is_admin": user_dto.is_admin,
                    "is_superuser": user_dto.is_superuser,
                }
            )
        except ApplicationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            if isinstance(e, NotFoundError):
                status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(e, ConflictError):
                status_code = status.HTTP_409_CONFLICT

            return Response({"message": e.message, "extra": e.extra}, status=status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePassword(ApiAuthMixin, APIView):
    """
    API endpoint for changing user password.
    Uses ChangePasswordUseCase from application layer.
    """

    class InputSerializer(serializers.Serializer):
        old_password = serializers.CharField()
        password1 = serializers.CharField()
        password2 = serializers.CharField()

        # def validate_old_password(self, value):
        #     user = self.context["request"].user
        #     if not user.check_password(value):
        #         raise serializers.ValidationError(
        #             _("Your old password was entered incorrectly. Please enter it again.")
        #         )
        #     return value

        def validate(self, data):
            if data["password1"] != data["password2"]:
                raise serializers.ValidationError({"password2": _("The two password fields didn't match.")})

            return data

    def post(self, request):
        serializer = self.InputSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        container = get_container()
        use_case = container.change_password_use_case

        try:
            use_case.execute(
                user_id=request.user.id,
                old_password=serializer.validated_data["old_password"],
                new_password=serializer.validated_data["password1"],
            )
            return Response({"message": "Password changed successfully"})
        except ApplicationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            if isinstance(e, NotFoundError):
                status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(e, ConflictError):
                status_code = status.HTTP_409_CONFLICT

            return Response({"message": e.message, "extra": e.extra}, status=status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
