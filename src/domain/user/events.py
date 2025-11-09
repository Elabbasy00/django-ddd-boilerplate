"""
User domain events.
"""

from src.domain.shared.events import DomainEvent
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class UserCreatedEvent(DomainEvent):
    """Event raised when a user is created."""

    username: str
    email: str


@dataclass
class UserUpdatedEvent(DomainEvent):
    """Event raised when a user is updated."""

    user_id: int
    updated_fields: list


@dataclass
class UserActivatedEvent(DomainEvent):
    """Event raised when a user is activated."""

    user_id: int


@dataclass
class UserDeactivatedEvent(DomainEvent):
    """Event raised when a user is deactivated."""

    user_id: int


@dataclass
class PasswordChangedEvent(DomainEvent):
    """Event raised when a user's password is changed."""

    user_id: int
