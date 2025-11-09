from typing import Optional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from src.application.shared.dtos import AuthenticationResultDTO, UserDTO
from src.domain.user.repositories import UserRepository
from src.domain.authentication.services import AuthenticationDomainService
from src.application.user.use_cases import GetUserUseCase


class AuthenticateUserUseCase:
    """
    Use case for authenticating a user.
    """

    def __init__(self, user_repository: UserRepository, auth_domain_service: AuthenticationDomainService):
        self._user_repository = user_repository
        self._auth_domain_service = auth_domain_service

    def execute(self, username: str, password: str) -> Optional[AuthenticationResultDTO]:
        """
        Authenticate a user with email and password.
        Returns AuthenticationResultDTO if successful, None otherwise.
        """
        # Use Django's authenticate (which handles password checking)
        # In a pure DDD approach, we'd do this in the domain, but Django's
        # authentication is tightly coupled to the ORM, so we use it here
        django_user = authenticate(username=username, password=password)

        if django_user is None:
            return None

        # Get domain user
        user = self._user_repository.get_by_id(django_user.id)
        if user is None:
            return None

        # Check if user can authenticate
        if not self._auth_domain_service.can_user_authenticate(user):
            return None

        # Convert to DTO
        user_dto = self._user_to_dto(user)

        return AuthenticationResultDTO(user=user_dto)

    @staticmethod
    def _user_to_dto(user) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
        )


class AuthenticateUserJWTUseCase:
    """
    Use case for authenticating a user and generating JWT tokens.
    """

    def __init__(self, user_repository: UserRepository, auth_domain_service: AuthenticationDomainService):
        self._user_repository = user_repository
        self._auth_domain_service = auth_domain_service

    def execute(self, username: str, password: str) -> Optional[AuthenticationResultDTO]:
        """
        Authenticate a user and generate JWT tokens.
        Returns AuthenticationResultDTO with tokens if successful, None otherwise.
        """
        # Use Django's authenticate
        django_user = authenticate(username=username, password=password)

        if django_user is None:
            return None

        # Get domain user
        user = self._user_repository.get_by_id(django_user.id)
        if user is None:
            return None

        # Check if user can authenticate
        if not self._auth_domain_service.can_user_authenticate(user):
            return None

        # Generate JWT tokens
        refresh = RefreshToken.for_user(django_user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Convert to DTO
        user_dto = self._user_to_dto(user)

        return AuthenticationResultDTO(user=user_dto, access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def _user_to_dto(user) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
        )
