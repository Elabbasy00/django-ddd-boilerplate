"""
Domain event publisher implementation.
"""

import logging
from typing import List, Dict, Type
from src.domain.shared.events import DomainEvent, DomainEventPublisher

logger = logging.getLogger(__name__)


class InMemoryEventPublisher(DomainEventPublisher):
    """
    In-memory event publisher with event type filtering.
    """

    def __init__(self):
        self._events: List[DomainEvent] = []
        # Group subscribers by event type for better performance
        self._subscribers_by_type: Dict[Type[DomainEvent], List[callable]] = {}
        # Subscribers that listen to all events
        self._all_subscribers: List[callable] = []

    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        self._events.append(event)
        event_type = type(event)

        # Notify type-specific subscribers
        if event_type in self._subscribers_by_type:
            for subscriber in self._subscribers_by_type[event_type]:
                self._notify_subscriber(subscriber, event)

        # Notify all-event subscribers
        for subscriber in self._all_subscribers:
            self._notify_subscriber(subscriber, event)

    def _notify_subscriber(self, subscriber: callable, event: DomainEvent) -> None:
        """Notify a subscriber with error handling."""
        try:
            subscriber(event)
        except Exception as e:
            logger.error(
                f"Error handling event {event.__class__.__name__} in {subscriber.__name__}: {e}",
                exc_info=True,
            )
            # Don't fail the operation if event handling fails

    def subscribe(self, handler: callable, event_type: Type[DomainEvent] = None) -> None:
        """
        Subscribe to domain events.

        Args:
            handler: Function to call when event is published
            event_type: Specific event type to subscribe to (optional).
                       If None, subscribes to all events.
        """
        if event_type:
            # Subscribe to specific event type
            if event_type not in self._subscribers_by_type:
                self._subscribers_by_type[event_type] = []
            self._subscribers_by_type[event_type].append(handler)
        else:
            # Subscribe to all events
            self._all_subscribers.append(handler)

    def get_events(self) -> List[DomainEvent]:
        """Get all published events (for testing/debugging)."""
        return self._events.copy()

    def clear_events(self) -> None:
        """Clear all events (for testing)."""
        self._events.clear()
