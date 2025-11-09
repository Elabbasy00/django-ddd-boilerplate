"""
User domain entity.
"""

from dataclasses import dataclass
from typing import Optional, Any
from src.domain.shared.entities import DomainEntity


@dataclass
class User(DomainEntity):
    """
    User aggregate root.
    Represents a user in the system.
    """

    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_staff: bool = False
    is_admin: bool = False
    is_superuser: bool = False
    password: Optional[str] = None

    def __post_init__(self):
        """Validate user entity after initialization."""
        if not self.username:
            raise ValueError("Username is required")
        if not self.email:
            raise ValueError("Email is required")

        # Normalize email
        self.email = self.email.lower().strip()

        # Validate username format
        import re

        username_pattern = r"^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$"
        if not re.match(username_pattern, self.username):
            raise ValueError("Invalid username format")

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False

    def promote_to_admin(self) -> None:
        """Promote user to admin."""
        self.is_admin = True

    def demote_from_admin(self) -> None:
        """Demote user from admin."""
        self.is_admin = False
