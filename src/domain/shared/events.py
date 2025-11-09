"""
Domain events for event-driven architecture.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass
class DomainEvent(ABC):
    """
    Base class for all domain events.
    Events represent something that happened in the domain.
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    occurred_at: datetime = field(default_factory=datetime.now, kw_only=True)
    aggregate_id: Any = field(default=None, kw_only=True)


class DomainEventPublisher(ABC):
    """
    Interface for publishing domain events.
    """

    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        pass
