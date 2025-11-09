"""
User repository interface (port).
"""

from abc import abstractmethod
from typing import Optional, List
from src.domain.shared.repositories import Repository
from src.domain.user.entities import User


class UserRepository(Repository[User]):
    """
    Repository interface for User aggregate.
    """

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        pass

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Check if a user exists with the given username."""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        pass

    @abstractmethod
    def get_active_users(self) -> List[User]:
        """Retrieve all active users."""
        pass
