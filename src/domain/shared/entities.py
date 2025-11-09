"""
Shared base entities for the domain layer.
"""

from abc import ABC
from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class DomainEntity(ABC):
    """
    Base class for all domain entities.
    Entities have identity and lifecycle.
    """

    id: Optional[Any] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        # Ensure updated_at is initialized
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Base class for value objects.
    Value objects are immutable and defined by their attributes.
    """

    pass
