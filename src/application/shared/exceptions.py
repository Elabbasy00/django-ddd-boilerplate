"""
Application layer exceptions.
These exceptions represent application-level errors.
Application layer can depend on domain exceptions.
"""

from typing import Optional, Dict, Any
from src.domain.shared.exceptions import DomainException


class ApplicationError(Exception):
    """
    Base exception for all application-level errors.

    This is the main exception class used throughout the application layer.
    It can wrap domain exceptions or represent application-specific errors.
    """

    def __init__(self, message: str, extra: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}

    def __str__(self) -> str:
        return self.message


class ValidationError(ApplicationError):
    """Raised when application-level validation fails."""

    pass


class NotFoundError(ApplicationError):
    """Raised when a resource is not found."""

    pass


class UnauthorizedError(ApplicationError):
    """Raised when an operation is unauthorized."""

    pass


class ConflictError(ApplicationError):
    """Raised when there's a conflict (e.g., duplicate resource)."""

    pass
