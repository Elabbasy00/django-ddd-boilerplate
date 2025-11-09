"""
Authentication domain entities.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Any
from src.domain.shared.entities import DomainEntity


@dataclass
class AuthenticationToken(DomainEntity):
    """
    Represents an authentication token.
    """

    user_id: int
    token: str
    refresh_token: Optional[str] = None
    expires_at: datetime = None
    token_type: str = "Bearer"
    is_revoked: bool = False

    def __post_init__(self):
        """Set default expiration if not provided."""
        if self.expires_at is None:
            self.expires_at = datetime.now() + timedelta(hours=1)

    def is_expired(self) -> bool:
        """Check if the token is expired."""
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the token is valid (not expired and not revoked)."""
        return not self.is_expired() and not self.is_revoked

    def revoke(self) -> None:
        """Revoke the token."""
        self.is_revoked = True


@dataclass
class Session(DomainEntity):
    """
    Represents a user session.
    """

    user_id: int
    session_key: str
    id: Optional[Any] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True

    def is_expired(self) -> bool:
        """Check if the session is expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the session is valid."""
        return self.is_active and not self.is_expired()

    def deactivate(self) -> None:
        """Deactivate the session."""
        self.is_active = False
