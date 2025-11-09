"""
Data Transfer Objects (DTOs) for the application layer.
"""

from dataclasses import dataclass
from typing import Optional

# from datetime import datetime


@dataclass
class UserDTO:
    """Data Transfer Object for User."""

    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_staff: bool
    is_admin: bool
    is_superuser: bool


@dataclass
class UserCreateDTO:
    """DTO for creating a user."""

    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class UserUpdateDTO:
    """DTO for updating a user."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class AuthenticationResultDTO:
    """DTO for authentication results."""

    user: UserDTO
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    session_key: Optional[str] = None


@dataclass
class ChangePasswordDTO:
    """DTO for changing password."""

    old_password: str
    new_password: str
    confirm_password: str
