"""
User domain services.
Contains business logic that doesn't naturally fit in the User entity.
"""

from typing import Optional
from src.domain.user.entities import User
from src.domain.user.repositories import UserRepository
from src.domain.user.value_objects import Email, Username


class UserDomainService:
    """
    Domain service for user-related business logic.
    """

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def is_email_unique(self, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if an email is unique.
        Optionally exclude a user ID (useful for updates).
        """
        existing_user = self._user_repository.get_by_email(email)

        if existing_user is None:
            return True

        if exclude_user_id and existing_user.id == exclude_user_id:
            return True

        return False

    def is_username_unique(self, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if a username is unique.
        Optionally exclude a user ID (useful for updates).
        """
        existing_user = self._user_repository.get_by_username(username)

        if existing_user is None:
            return True

        if exclude_user_id and existing_user.id == exclude_user_id:
            return True

        return False

    def validate_user_creation(self, username: str, email: str) -> None:
        """
        Validate that a user can be created with the given username and email.
        Raises DomainException if validation fails.
        """
        from src.domain.shared.exceptions import BusinessRuleViolationError

        # Validate value objects
        try:
            Username(username)
        except ValueError as e:
            raise BusinessRuleViolationError(f"Invalid username: {str(e)}")

        try:
            Email(email)
        except ValueError as e:
            raise BusinessRuleViolationError(f"Invalid email: {str(e)}")

        # Check uniqueness
        if not self.is_username_unique(username):
            raise BusinessRuleViolationError(f"Username '{username}' is already taken")

        if not self.is_email_unique(email):
            raise BusinessRuleViolationError(f"Email '{email}' is already taken")
