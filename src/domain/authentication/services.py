"""
Authentication domain services.
"""

from typing import Optional
from src.domain.user.entities import User
from src.domain.user.repositories import UserRepository


class AuthenticationDomainService:
    """
    Domain service for authentication-related business logic.
    """

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def authenticate_user(self, username: str, password_hash: str) -> Optional[User]:
        """
        Authenticate a user by username and password hash.
        Returns the user if authentication succeeds, None otherwise.
        """
        user = self._user_repository.get_by_username(username)

        if user is None:
            return None

        if not user.is_active:
            return None

        # Note: In a real implementation, you'd verify the password hash here
        # This is a simplified version - the actual password verification
        # should happen in the application layer using Django's password checking
        return user

    def can_user_authenticate(self, user: User) -> bool:
        """
        Check if a user can authenticate (is active, etc.).
        """
        return user.is_active
