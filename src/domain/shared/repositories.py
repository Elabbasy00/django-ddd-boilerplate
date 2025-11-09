"""
Repository interfaces (ports) for the domain layer.
These define contracts that infrastructure will implement.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar
from src.domain.shared.entities import DomainEntity

T = TypeVar("T", bound=DomainEntity)


class Repository(ABC, Generic[T]):
    """
    Base repository interface.
    All domain repositories should inherit from this.
    """

    @abstractmethod
    def get_by_id(self, entity_id: any) -> Optional[T]:
        """Retrieve an entity by its ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all entities."""
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        """Save or update an entity."""
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        """Delete an entity."""
        pass


class UnitOfWork(ABC):
    """
    Unit of Work pattern interface.
    Ensures transactional consistency.
    """

    @abstractmethod
    def __enter__(self):
        """Enter the unit of work context."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the unit of work context."""
        pass

    @abstractmethod
    def commit(self):
        """Commit all changes."""
        pass

    @abstractmethod
    def rollback(self):
        """Rollback all changes."""
        pass
