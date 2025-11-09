"""
User domain value objects.
"""

from dataclasses import dataclass
from src.domain.shared.entities import ValueObject
import re


@dataclass(frozen=True)
class Email(ValueObject):
    """
    Email value object with validation.
    """

    value: str

    def __post_init__(self):
        """Validate email format."""
        if not self.value:
            raise ValueError("Email cannot be empty")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.value):
            raise ValueError("Invalid email format")

        # Normalize email
        object.__setattr__(self, "value", self.value.lower().strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Username(ValueObject):
    """
    Username value object with validation.
    """

    value: str

    def __post_init__(self):
        """Validate username format."""
        if not self.value:
            raise ValueError("Username cannot be empty")

        username_pattern = r"^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$"
        if not re.match(username_pattern, self.value):
            raise ValueError("Invalid username format")

    def __str__(self) -> str:
        return self.value
