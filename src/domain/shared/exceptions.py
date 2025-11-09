"""
Domain layer exceptions.
These exceptions represent domain-level errors and business rule violations.
"""

from typing import Optional, Dict, Any


class DomainException(Exception):
    """
    Base exception for all domain errors.
    Domain exceptions represent business rule violations.
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return self.message


class EntityNotFoundError(DomainException):
    """Raised when a domain entity is not found."""

    pass


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    pass


class InvalidValueError(DomainException):
    """Raised when a value object validation fails."""

    pass
